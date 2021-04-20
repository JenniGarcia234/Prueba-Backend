import ast
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api_c.models import Lessons, LogScoreStudent, ScoreStudent, LogQuestionUser, User, Questions, Answers, Course
from api_c.serializers import LessonSerializer, QuestionsSerializer, AnswersSerializer, SpecificQuestionSerializer, \
    GetAnswersSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from api_c.permissions import IsProfessor, IsStudent


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def lessons_list(request):
    if request.method == 'GET':
        items = Lessons.objects.all()
        serializer = LessonSerializer(items, many=True)
        return Response(dict(success=True, data=serializer.data))

    elif request.method == 'POST':
        return add_lesson(request)


@permission_classes((IsProfessor ))
def add_lesson(request):
    serializer = LessonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(dict(success=True, data=serializer.data), status=201)
    return Response(dict(success=False, errors=serializer.errors), status=400)



@api_view(['GET', 'PUT', 'DELETE'])

@permission_classes((IsAuthenticated, ))
def lessons_detail(request, pk):
    try:
        item = Lessons.objects.get(pk=pk)
    except Lessons.DoesNotExist:
        return Response(dict(success=False, erros=["No existe esa lección"]), status=400)

    if request.method == 'GET':
        serializer = LessonSerializer(item)
        return Response(dict(success=True, data=serializer.data))

    else:
        return edit_lesson(request, item)


@permission_classes((IsAuthenticated, IsProfessor))
def edit_lesson(request, item):
    if request.method == 'PUT':
        serializer = LessonSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(dict(success=True, data=serializer.data))
        return Response(dict(success=False, erros=[serializer.errors]), status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def lessons_by_course(request, course):
    items = Lessons.objects.filter(course=course)
    serializer = LessonSerializer(items, many=True)
    return Response(dict(success=True, data=serializer.data))




@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def lesson_user_can_access(request, lesson):
    students_pass_lesson = set(LogScoreStudent.objects.filter(lesson=lesson).values_list('owner', flat=True))
    student_actualy_lesson = set(ScoreStudent.objects.filter(lesson=lesson).values_list('owner', flat=True))
    resp = (students_pass_lesson | student_actualy_lesson)
    return Response(dict(success=True, data=resp), status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def all_answer_in_one_go(request):
    try:
        questions_answers = ast.literal_eval(request.POST.get('questions_answers', ''))
        studend_id = request.POST.get('student', '')
        lesson = request.POST.get('lesson', '')
        questions = Questions.objects.filter(lessons=lesson)
        try:
            item_lesson = Lessons.objects.get(pk=lesson)
        except Exception as e:
            print (e)
            return Response(dict(success=False, data=["No existe esa lección"]), status=400)

        for question in questions:
            errors = []
            success = True
            if questions_answers and question.pk in questions_answers:
                print (question.pk)
                errors = validate(studend_id, question.pk, item_lesson)
                success = len(errors) == 0
                print (success)
                print (errors)
                if not success:
                    return Response(dict(success=success, errors=errors), status=400)
                else:
                    check_questions(studend_id, question.pk, questions_answers[question.pk])
            else:

                return Response(dict(success=False, errors=["No tiene todas las preguntas de la lección"]), status=400)
        return validate_score(studend_id)
    except Exception as e:
        return Response(dict(success=False, errors=["No tiene el formato descrito"]), status=400)


def validate_score(student):
    try:
        item_student = User.objects.get(pk=student)
    except User.DoesNotExist:
        return Response(dict(success=False, errors=["No existe ese usuario"]), status=400)
    item_score_student = ScoreStudent.objects.get(owner=student)
    item_questions_answered_user = LogQuestionUser.objects.filter(owner=item_student.pk,
                                                                  lesson=item_score_student.lesson).values_list(
        'question', flat=True)
    item_course = Course.objects.get(pk=item_score_student.course.pk)
    item_lesson = Lessons.objects.get(pk=item_score_student.lesson.pk)
    questions_not_answered = Questions.objects.filter(lessons=item_score_student.lesson).exclude(
        id__in=item_questions_answered_user)
    if item_score_student.score >= item_lesson.approval_score:
        LogScoreStudent(owner=item_student, course=item_score_student.course, lesson=item_lesson,
                        score=item_score_student.score).save()
        if item_lesson.next_one is not None:
            ScoreStudent.objects.filter(owner=student).update(lesson=item_lesson.next_one,
                                                                score=0)
            return Response(dict(success=False, data="Has terminado la lección"), status=200)

        else:
            if item_course.next_one is not None:
                item_first_lesson = Lessons.objects.get(previous_one=None, course=item_course.next_one)
                ScoreStudent.objects.filter(owner=student).update(lesson=item_first_lesson,
                                                                    course=item_course.next_one, score=0)
                return Response(dict(success=False, data="Has avanzado de curso"), status=200)
            else:
                return Response(dict(success=False, data="Has terminado todos los cursos"), status=200)
    else:
        return Response(dict(success=False, errors=["No alcancaste los puntos para pasar de lección"]), status=400)


def validate(user_id, question, item_lesson):
    errors = []
    if item_lesson.previous_one is not None:
        try:
            LogScoreStudent.objects.get(owner=user_id, lesson=item_lesson.previous_one)
        except LogScoreStudent.DoesNotExist:
            errors.append('No tiene acceso para esta lección')
    try:
        LogQuestionUser.objects.get(owner=user_id, question=question)
        errors.append('Esa pregunta ya ha sido contestada')
    except LogQuestionUser.DoesNotExist:
        pass
    try:
        User.objects.get(pk=user_id)
    except User.DoesNotExist:
        errors.append('No existe ese usuario')
    try:
        item_question = Questions.objects.get(pk=question)
    except Questions.DoesNotExist:
        errors.append('No existe esa pregunta')

    items_answers = Answers.objects.filter(question=item_question.pk, correct=True)
    if len(items_answers) == 0:
        errors.append('No existen respuestas para esa pregunta')
    return errors


def check_questions(user_id, question, response):
    LogQuestionUser.objects.get(owner=user_id, question=question)
    item_user = User.objects.get(pk=user_id)
    item_question = Questions.objects.get(pk=question)

    items_answers = Answers.objects.filter(question=item_question.pk, correct=True)
    if item_question.type == "BO" or item_question.type == "MC1C":
        validate_question_BO_MC1C(item_user, items_answers, item_question, response)
    elif item_question.type == "MCWC":
        validate_question_MCWC(item_user, items_answers, item_question, response)
    elif item_question.type == "MCAC":
        validate_question_MCAC(item_user, items_answers, item_question, response)


def validate_question_BO_MC1C(item_user, items_answers, item_question, response):
    if items_answers[0].pk == response[0]:
        LogQuestionUser(owner=item_user, question=item_question, lesson=item_question.lessons, correct=True).save()
    else:
        print (False)
        LogQuestionUser(owner=item_user, question=item_question, lesson=item_question.lessons, correct=False).save()


def validate_question_MCWC(item_user, items_answers, item_question, response):
    for item_answers in items_answers:
        if item_answers.correct:
            if item_answers.pk in response:
                LogQuestionUser(owner=item_user, question=item_question, lesson=item_question.lessons,
                                correct=True).save()
    LogQuestionUser(owner=item_user, question=item_question, lesson=item_question.lessons, correct=False).save()


def validate_question_MCAC(item_user, items_answers, item_question, response):
    for item_answers in items_answers:
        if item_answers.correct:
            if item_answers.pk in response:
                response.remove(item_answers.pk)
    print (len(response))
    if not response:
        LogQuestionUser(owner=item_user, question=item_question, lesson=item_question.lessons, correct=True).save()
    else:
        LogQuestionUser(owner=item_user, question=item_question, lesson=item_question.lessons, correct=False).save()


@api_view(['GET'])
@permission_classes((IsProfessor, ))
def lesson_detail_answering_question(request, lesson):
    questions = Questions.objects.filter(lessons=lesson)
    response = []
    for question in questions:
        temp={}
        temp["question"] = SpecificQuestionSerializer(question).data
        answers = []
        items_answers =  Answers.objects.filter(question=question.pk)
        for item_answer in items_answers:
            answers.append(GetAnswersSerializer(item_answer).data)
        temp["answer"] = answers
        response.append(temp)
    return Response(response)