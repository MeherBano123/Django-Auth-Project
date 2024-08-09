from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from account.views import (UserRegistrationView,UserLoginView,
                           UserProfileView,UserChangePasswordView,
                           SendPasswordResetEmailView,UserPasswordResetView,UserCoursesView,
                            UserListCreateView, UserRetrieveUpdateDestroyView,
                            StudentListView, StudentRetrieveUpdateDestroyView,
                            InstructorListView, InstructorRetrieveUpdateDestroyView,
                            CourseListCreateView, CourseRetrieveUpdateDestroyView,UserSearchView
                            )

urlpatterns = [
    path('user/register/', UserRegistrationView.as_view(),name="register"),
    path('user/login/',UserLoginView.as_view(),name='login'),
    path('user/profile/',UserProfileView.as_view(),name='profile'),
    path('user/changepassword/',UserChangePasswordView.as_view(),name='change-password '),
    path('user/send-reset-password-email/',SendPasswordResetEmailView.as_view(),name='send-reset-password-email'),
    path('user/password-reset/<uid>/<token>/',UserPasswordResetView.as_view(),name='reset-password'),
    path('user-courses/<str:email>/',UserCoursesView.as_view(),name='user-courses'),

    #Paths of  CRUD apis 
    
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),

    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentRetrieveUpdateDestroyView.as_view(), name='student-retrieve-update-destroy'),

    
    path('instructors/', InstructorListView.as_view(), name='instructor-list'),
    path('instructors/<int:pk>/', InstructorRetrieveUpdateDestroyView.as_view(), name='instructor-retrieve-update-destroy'),

   
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view(), name='course-retrieve-update-destroy'),

    path('api/users/search/', UserSearchView.as_view(), name='user-search')
   
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
