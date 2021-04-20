
import ast
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api_c.models import Answers, Questions
from api_c.serializers import AnswersSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from api_c.permissions import IsProfessor


@api_view(['GET', 'POST'])
@permission_classes((IsProfessor, ))
def answers_list(request):
    if request.method == 'GET':
        items = Answers.objects.all()
        serializer = AnswersSerializer(items, many=True)
        return Response(dict(success=True, data=serializer.data))

    elif request.method == 'POST':
        return add_answer(request)



def add_answer(request):

    """Metodo para agregar preguntas, en caso de ser tipo BO, en corrects solo se acepta [0] para respuestas False y
    [1] para respuestas True """
    question = request.POST.get("question", "")
    values = ast.literal_eval(request.POST.get("values", ""))
    corrects = ast.literal_eval(request.POST.get("corrects", ""))
    if len(corrects) < 1:
        return Response(dict(success=False, error=["Debe agregar al menos una respuesta correcta"]), status=400)
    cont = 1
    try:
        item_queston = Questions.objects.get(pk=question)
        Answers.objects.filter(question=question).delete()
        if item_queston.type == "BO":
            Answers(question=item_queston, value=corrects[0] == True, correct=True).save()
            Answers(question=item_queston, value=corrects[0] != True, correct=False).save()
            return Response(status=204)
    except Questions.DoesNotExist:
        return Response(dict(success=False, error=["No se encuentra la pregunta"]), status=400)
    for answer in values:
        try:
            if cont in corrects:
                answer = Answers(question=item_queston, value=answer, correct=True)
            else:
                answer = Answers(question=item_queston, value=answer, correct=False)
            answer.save()
        except Exception as e:
            print (e)
        cont += 1
    return Response(status=204)


@api_view(['GET', 'DELETE'])
@permission_classes((IsProfessor,))
def answers_detail(request, question):

    try:
        items = Answers.objects.filter(question=question)
        if len(items) < 1:
            return Response(dict(success=False, error=["No se encuentran respuesta a esa pregunta"]), status=400)

    except Answers.DoesNotExist:
        return Response(dict(success=False, error=["No se encuentra esa respuesta"]), status=400)

    if request.method == 'GET':
        serializer = AnswersSerializer(items, many=True)
        return Response(dict(success=True, data=serializer.data))
    else:
        return dete_answer(request, items)



def dete_answer(request, items):
    if request.method == 'DELETE':
        items.delete()
        return Response(status=204)