from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.views import APIView
from .models import Course, Enrollment,User

from rest_framework_simplejwt.authentication import JWTAuthentication
from account.serializers import (UserRegistrationSerializer,UserLoginSerializer,
                                  UserProfileSerializer,UserChangePasswordSerializer,
                                  SendPasswordResetEmailSerializer,UserPasswordResetSerializer,
                                  CourseSerializer,EnrollmentSerializer,
                                  UserSerializer)
from django.contrib.auth import authenticate
from account.renderers import UserRenderer,InstructorRenderer,CoursesRenderer,EnrollmentRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

#creating tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            #token is created for new user
            token=get_tokens_for_user(user)
            return Response({"token":token,"msg":"registration success"},
                            status=status.HTTP_201_CREATED)
        #errors are printed when raise_exception is missing
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   

class UserLoginView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                #token is created for logged in user
               # token=get_tokens_for_user(user)
                return Response({"msg":"Login success"},
                            status=status.HTTP_200_OK)
            else:
                return Response({'errors' : {'non_field_errors':['Email or Password is not valid']}}
                            ,status=status.HTTP_404_NOT_FOUND)



class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,fomat=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
       


class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,fomat=None):
        serializer=UserChangePasswordSerializer(data=request.data,context={"user":request.data})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Changed Password"},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,fomat=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password Reset Link sent, please check your Email"},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, uid, token, fomat=None):
        serializer=UserPasswordResetSerializer(data=request.data,
                                                context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
             return Response({"msg":"Password Reset successfully"},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

       

# List Courses for a User
class UserCoursesView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        # Get the email from the URL path parameter
        user_email = self.kwargs.get('email')
        if user_email:
            # Filter enrollments by the provided email
            enrollments = Enrollment.objects.filter(userEmail__email=user_email)
            return enrollments
        return Enrollment.objects.none()  

        

#CRUD APIs for user,students,instructor,courses
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
   

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
# Student Views
class StudentListView(generics.ListAPIView):
    serializer_class = UserSerializer
    

    def get_queryset(self):
        return User.objects.filter(is_student=True)

class StudentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_student=True)
    serializer_class = UserSerializer
   

# Instructor Views
class InstructorListView(generics.ListAPIView):
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return User.objects.filter(is_instructor=True)

class InstructorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_instructor=True)
    serializer_class = UserSerializer
    

# Course Views
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    

class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
   

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    

    def get_queryset(self):
        queryset = User.objects.all()
        email = self.request.query_params.get('email', None)
        first_name = self.request.query_params.get('first_name', None)
        last_name = self.request.query_params.get('last_name', None)
        phone_no = self.request.query_params.get('phone_no', None)

        if email:
            queryset = queryset.filter(email__icontains=email)
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if phone_no:
            queryset = queryset.filter(phone_no__icontains=phone_no)

        return queryset

