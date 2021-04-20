from django.db import models
from datetime import date
import datetime
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Los usuarios deben tener un nombre de usuario')
        if email is None:
            raise TypeError('Los usuarios deben tener un email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Debe ingresar una contraseña')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}
 
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    firstname = models.CharField(max_length=124)
    lastname = models.CharField(max_length=45, blank=True, null=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin= models.BooleanField(default=False)
    is_professor=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)
    created_at = models.DateTimeField(null=False, blank=False,auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)




    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Course(models.Model):
    title = models.CharField(max_length=200)
    previous_one= models.ForeignKey("Course", related_name="previousOne", on_delete=models.SET_NULL, blank=True, null=True)
    next_one= models.ForeignKey("Course", related_name="nextOne", on_delete=models.SET_NULL, blank=True, null=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-updated_at']


    def save(self, *args, **kwargs):

        try:
            if self.id is None:
                previous_course = Course.objects.get(next_one=None)
                self.previous_one = previous_course
                super(Course, self).save(*args, **kwargs)
                previous_course.next_one = self
                previous_course.save()
            else:
                super(Course, self).save(*args, **kwargs)
        except:
            super(Course, self).save(*args, **kwargs)

    def delete(self):
        try:
            course = Course.objects.get(pk=self.previous_one.pk)
            course.next_one = self.next_one
            course.save()
        except:
            pass
        try:
            course = Course.objects.get(pk=self.next_one.pk)
            course.previous_one = self.previous_one
            course.save()
        except:
            pass
        super(Course, self).delete()



class InscriptionStudent(models.Model):
    student= models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    course= models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    status= models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: ['-created_at']

    def __str__(self):
        return str(self.student)+'s inscription'

class Lessons(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    previous_one = models.ForeignKey("Lessons", related_name="previousOne", on_delete=models.SET_NULL, blank=True,
                                     null=True)
    next_one = models.ForeignKey("Lessons", related_name="nextOne", blank=True, on_delete=models.SET_NULL, null=True)
    approval_score = models.IntegerField()
    owner = models.ForeignKey(to=User, blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'lessons'

    def save(self, *args, **kwargs):
        try:
            if self.id is None:
                previous_lesson = Lessons.objects.get(next_one=None, course=self.course)
                self.previous_one = previous_lesson
                super(Lessons, self).save(*args, **kwargs)
                previous_lesson.next_one = self
                previous_lesson.save()
            else:
                super(Lessons, self).save(*args, **kwargs)
        except:
            super(Lessons, self).save(*args, **kwargs)

    def delete(self):
        try:
            lesson = Lessons.objects.get(pk=self.previous_one.pk)
            lesson.next_one = self.next_one
            lesson.save()
        except:
            pass
        try:
            lesson = Lessons.objects.get(pk=self.next_one.pk)
            lesson.previous_one = self.previous_one
            lesson.save()
        except:
            pass
        super(Lessons, self).delete()

class Questions(models.Model):
    A = "BO"
    B = "MC1C"
    C = "MCWC"
    D = "MCAC"
    TYPE_ANSWER_CHOICE = (
        (A, 'Boolean'),
        (B, 'Multiple choice one correct'),
        (C, 'Multiple choice more than one is correct'),
        (D, 'Multiple choice more than one answer is correct all of them mustbe answered correctly'),
    )
    question = models.CharField(max_length=500, blank= True, null= True)
    lessons = models.ForeignKey(Lessons, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=4, choices=TYPE_ANSWER_CHOICE)
    owner= models.ForeignKey(to=User, blank=True, null=True, on_delete=models.SET_NULL)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-created_at']

    def __str__(self):
        return str(self.owner)+'s question'


#Answers model 
class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, blank=True, null=True)
    value = models.TextField()
    correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-created_at']

    def __str__(self):
        return str(self.question)


class LogQuestionUser(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Questions, on_delete=models.SET_NULL, blank=True, null=True)
    lesson = models.ForeignKey(Lessons,on_delete=models.SET_NULL,blank=True,null=True)
    correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-created_at']

    def save(self, *args, **kwargs):
        try:
            if self.correct:
                score_student = ScoreStudent.objects.get(owner=self.owner.pk)
                score_student.score = score_student.score + self.question.score
                score_student.save()
            super(LogQuestionUser, self).save(*args, **kwargs)
        except:
            pass
        

class ScoreStudent(models.Model):
    owner= models.ForeignKey(to=User,on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(to=Course, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(to=Lessons, on_delete=models.SET_NULL, null=True)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-created_at']


class LogScoreStudent(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    course = models.ForeignKey(to=Course, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(to=Lessons, on_delete=models.SET_NULL, null=True)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-created_at']