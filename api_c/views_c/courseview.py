from rest_framework.decorators import api_view
from rest_framework.response import Response
from api_c.models import Course, LogScoreStudent, ScoreStudent
from api_c.serializers import CoursesSerializer, AddLessonsSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from api_c.permissions import IsProfessor, IsStudent

def order_course(id):
    pass



@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def courses_list(request):
    if request.method == 'GET':
        items = Course.objects.all()
        serializer = CoursesSerializer(items, many=True)
        return Response({'success': True, 'data': serializer.data})

    elif request.method == 'POST':
        return add_courses(request)



def add_courses(request):
    serializer = CoursesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response({'success': True, 'data': serializer.data}, status=201)
    return Response({'success': False, 'errors': serializer.errors}, status=400)



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsProfessor, ))
def courses_detail(request, pk):
    try:
        item = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(dict(success=False, errors=['No existe ese Curso']), status=400)

    if request.method == 'GET':
        serializer = CoursesSerializer(item)
        return Response(dict(success=True, data=serializer.data))

    else:
        return edit_course(request, item)



def edit_course(request, item):
    if request.method == 'PUT':
        serializer = CoursesSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(dict(success=True, data=serializer.data))
        return Response(dict(success=False, errors=[serializer.errors]), status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)



@api_view(['GET'])
@permission_classes((IsProfessor, IsAuthenticated))
def courses_user_can_access(request, course):
    students_pass_course = set(LogScoreStudent.objects.filter(course=course).values_list('owner', flat=True))
    student_actualy_course = set(ScoreStudent.objects.filter(course=course).values_list('owner', flat=True))
    resp = (students_pass_course | student_actualy_course)
    return Response(dict(success=True, data=resp), status=200)
