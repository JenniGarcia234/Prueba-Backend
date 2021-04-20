from api_c.views_c import usersview, courseview, lessonview, questionview, answerview, scorestudentview
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import (
    TokenRefreshView,)
urlpatterns = [
#Register user
    path('register/', usersview.RegisterView.as_view(), name="register"),
#Login user
    path('login/', usersview.LoginAPIView.as_view(), name="login"),
#Get my profile professor
    path('my-profile-professor/', usersview.UserProfileProfessor.as_view(), name="my_profile_professor"),
#Get my profile student
    path('my-profile-student/', usersview.UserProfileStudent.as_view(), name="my_profile_student"),
#Update profile professor 
    path('my-profile-professor/update/<int:pk>', usersview.UserProfileUpdateProfessor.as_view(), name="update_profile_professor"),
#Update profile student
    path('my-profile-student/update/<int:pk>', usersview.UserProfileUpdateStudent.as_view(), name="update_profile_student"),
#Logout user
    path('logout/', usersview.LogoutAPIView.as_view(), name="logout"),
#token refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('password-reset/<uidb64>/<token>/',usersview.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', usersview.SetNewPasswordAPIView.as_view(),name='password-reset-complete'),

#Get students list
    path('students/', usersview.students_list),
#Get professors list
    path('professors/', usersview.professors_list),

#Get, put and delete course by course_id
    path('courses/<int:pk>',courseview.courses_detail),
#Get, post courses   
    path('courses/',courseview.courses_list),

#Get list of courses that students can access
    path('courses_user_can_access/<int:course>',courseview.courses_user_can_access),   
    

#Get and post a lesson
    path('lessons/',lessonview.lessons_list),
#Get, put and delete lessons per lesson_id and course_id
    path('lessons/<int:pk>',lessonview.lessons_detail),
#Get lesson by course
    path('lessons_by_course/<int:course>',lessonview.lessons_by_course),                   
##Get the list of students who can access a lesson
    path('lesson_user_can_access/<int:lesson>',lessonview.lesson_user_can_access),  
#All answers in one go 
    path('all_answer_in_one_go/',lessonview.all_answer_in_one_go),
#Get details of lesson, answers and questions
    path('lesson_detail_answering_question/<int:lesson>',lessonview.lesson_detail_answering_question),  



#Get and post a question 
    path('questions/<int:pk>',questionview.questions_detail),
#Get, patch and delete question 
    path('questions/',questionview.questions_list),
#Get questions by lesson
    path('questions_by_lesson/<int:lesson>',questionview.questions_by_lesson),
#Post answer-question student
    path('answer-question/',questionview.answer_question),
#Get questions for student
    path('questions_student/<int:student>',questionview.question_for_user),


#Get answer
    path('answers_questions/<int:question>', answerview.answers_detail),
#Add answers
    path('answers/', answerview.answers_list),


#Get scorestudent
    path('scorestudent/', scorestudentview.scorestudent_list),
#Detail
    path('scorestudent/<int:pk>', scorestudentview.scorestudent_detail),
]