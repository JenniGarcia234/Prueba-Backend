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


# Endpoints
#### /api_c/register/

Parameters: `email, username, password`

#### /api_c/login/

Parameters: `email, password`


#### /api_c/my-profile-professor/

Parameters: Authorization with token obtained when logging in

#### /api_c/my-profile-student/

Parameters: Authorization with token obtained when logging in


#### /api_c/my-profile-professor/update/pk

###Agregar una pregunta

#### /api_c/questions/
Parametros:
`question= id_question
values= Array con las respuestas posibles
correct= Array con las respuestas correctas, en caso de seleccionar pregunta de tipo booleano, el valor puede ser [0] o [1]`

### Agregar respuesta
Posterior, se procede a agregar las respuestas a dicha pregunta con el siguiente endpoint.

#### /api_c/answers/
Los parámetros son:
`question= id de la pregunta
values= array con las respuestas posibles, si el tipo de pregunta es Boolean entonces este campo puede ir vacio
correct= array con los elementos correctos del array values, si el tipo de pregunta es Boolean entonces
solo pueden haber 2 valores [0] para cuando la respuesta es False y [1] para cuando la respuesta es True`

Ejemplo tipo pregunta BO y como respuesta Verdadero:

`question= 1
values= []
correct=[1]`

Ejemplo tipo pregunta MC1C, respuesta correcta es values[3]=respuesta3 

`question= 1
values= ["respuesta1","respuesta2","respuesta3"]
correct=[3]
ejemplo tipo pregunta MCWC, respuesta correcta es values[3]=respuesta3 o values[1]=respuesta1 `

`question= 1
values= ["respuesta1","respuesta2","respuesta3"]
correct=[3,1]
ejemplo tipo pregunta MCAC, respuesta correcta es values[3]=respuesta3 y values[1]=respuesta1 `

`question= 1
values= ["respuesta1","respuesta2","respuesta3"]
correct=[3,1]
El enpoint elimina las respuestas actuales y agrega las que se estén enviando `

No se tiene un límite de respuestas posibles tampoco de respuestas correctas

### Responder todas las preguntas de una lección:
#### /api_c/all_answer_in_one_go/
Los parámetros son:

`questions_answers = dict con la forma {id_pregunta:[id_respuestas_seleccionadas]}
studen = id_estudiante
lesson = id_leccion
ejemplo contestada la lección 3 enviando id_respuestas[2,3,4] para id_preguna=1 y id_respuesta{3] para id_pregunta=2:

questions_answers = [{1:[2,3,4]},{2:[3]}]
student = 12
lesson = 3 `

#### Responder preguntas por el estudiante
Para obtener la pregunta:

#### api_c/question_for_user/<id_estudiante>

Para responder la pregunta:

#### api_c/answer_question/

Parámetros:

`student = id_estudiante
question =  id_pregunta
response = [id_respuestas]
Solo se debe envíar una lista con los id de las respuestas que el usuario haya seleccionado`



