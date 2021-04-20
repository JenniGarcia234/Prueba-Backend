from rest_framework import serializers
from .models import User, Course, Lessons, Questions, Answers, ScoreStudent
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'El nombre de usuario solo debe contener caracteres alfanuméricos'}

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
   


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Credenciales inválidas, intantalo de nuevo' )


        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)


#User profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','username', 'email', 'firstname', 'lastname']

class ProfileSerializerP(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','username', 'email', 'firstname', 'lastname']

class ProfileSerializerS(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','username', 'email', 'firstname', 'lastname']

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('El enlace de restablecimiento no es válido', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('El enlace de restablecimiento no es válido', 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('El token ha expirado o es inválido')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


#Course serializer
class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ('owner',)
        depth = 0


#Course detail serializer
class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ['update_at']

class AddAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['question','value','correct']




#Lesson serializer
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ['pk','title', 'description','course','previous_one','next_one', 'approval_score']

#Lesson detail serializer

class LessonDatailSerializer(serializers.ModelSerializer):
    class Meta:
        model: Lessons
        exclude =['update_at']



class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        depth = 0
        fields = '__all__'


class SpecificQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        exclude = ('created', 'updated','created_by','lessons')
        depth = 0


class GetQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        depth = 1
        fields = '__all__'


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        depth = 0
        fields = '__all__'


class GetAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        exclude = ('created', 'updated')
        depth = 0

class AddLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        depth = 0
        fields = '__all__'


class ScoreStudentSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = ScoreStudent
        depth = 1
        fields = '__all__'


class PutScoreStudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ScoreStudent
        depth = 0
        fields = '__all__'

#List all students
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','username', 'email', 'firstname', 'lastname']


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','username', 'email', 'firstname', 'lastname']