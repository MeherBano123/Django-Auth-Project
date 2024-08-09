
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Custom user manager
class UserManager(BaseUserManager):
    def create_user(self, email, first_name,last_name, tc,is_student, is_instructor,image=None, password=None,password2=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            tc=tc,
            image=image,
            is_student=is_student,
            is_instructor=is_instructor
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name,last_name, tc,is_student, is_instructor,image=None, password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            tc=tc,
            image=image,
            is_student=is_student,
            is_instructor=is_instructor
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(verbose_name="email address", max_length=255,unique=True)
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_student=models.BooleanField(default=False )
    is_instructor=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  
    phone_no=models.CharField(max_length=20,null=True)
    name=models.CharField(max_length=500,null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name","tc","is_student", "is_instructor"]
    class Meta:
        db_table = 'user_data'

    def name(self):
        name=self.first_name +" " +self.last_name
        return name
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin




    

class Course(models.Model):
    title = models.CharField(max_length=255,unique=True)
    description = models.TextField()
    students = models.ManyToManyField(User,related_name='courses_enrolled', blank=True)
    instructor  = models.ForeignKey(User, related_name='courses_taught', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    userEmail = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
    courseTitle = models.ForeignKey(Course, on_delete=models.CASCADE,to_field='title')
    enrolled_on = models.DateTimeField(auto_now_add=True)


