# Prueba-Backend
Backend developer position challenge

We require to develop an API for e-learning courses to integrate in our system. The purpose of this tool is for us, as professors to manage courses configuration and performance reviews and, for our students, to take courses when using our frontend. Our PM is a very busy person, so we don’t have detailed tasks but only the business rules to work with. Here they are:

We have courses that contain lessons and lessons that contain questions

The courses are correlative with previous ones

The lessons are correlative with previous ones

The questions for each lesson have no correlation

All questions for a lesson are mandatory

Each question has a score

Each lesson has an approval score that has to be met by the sum of correctly answered questions to approve it

A course is approved when all lessons are passed.

There’s no restriction on accessing approved courses

Only professors can create and manage courses, lessons and questions

Any student can take a course

Initially, we’ll need to support these types of questions:

Boolean
Multiple choice where only one answer is correct
Multiple choice where more than one answer is correct
Multiple choice where more than one answer is correct and all of them must be answered correctly
Frontend guys specifically asked for these endpoints for the students to use:

Get a list of all courses, telling which ones the student can access
Get lessons for a course, telling which ones the student can access
Get lesson details for answering its questions
Take a lesson (to avoid several requests, they asked to send all answers in one go)
Basic CRUD for courses, lessons and questions
Codebase rules:

The API must be developed using Python
There must be a readme file documenting installation and usage.
You can use any frameworks and libraries you want, but they must be included in the readme file documenting its purpose and a brief explanation with the reasoning for your choice.


#Endpoints

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

