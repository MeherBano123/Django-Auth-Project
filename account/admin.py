from django.contrib import admin
from account.models import User, Course,Enrollment
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#Custom UserAdmin
class UserModelAdmin(BaseUserAdmin):
    list_display = ["id", "email", "name", "tc", "is_admin","image","phone_no","is_student"]
    list_filter = ["is_admin","is_student"]
    fieldsets = [
        ("Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "tc","image","phone_no","is_student"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email",  "first_name","last_name", "tc", "password1",
                            "password2","image","phone_no","is_admin","is_student"],
            },
        ),
    ]
    search_fields = [ "first_name","last_name","email","phone_no"]
    ordering = ["id"]
    filter_horizontal = []
    

# Register the User model with the custom UserModelAdmin
admin.site.register(User, UserModelAdmin)


# Custom CoursesAdmin
class CoursesAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "instructor"]
    fieldsets = [
        ("Course Info", {"fields": ["title", "description", "instructor"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["title", "description", "instructor"]
            },
        ),
    ]
    search_fields = ["title","instructor"]
    ordering = ["id"]
    filter_horizontal = []

# Register the Courses model
admin.site.register(Course, CoursesAdmin)


# Custom Enrollment model
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["userEmail", "courseTitle"]
    fieldsets = [
        ("Enrollment Info", {"fields": ["userEmail", "courseTitle"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["userEmail", "courseTitle"],
            },
        ),
    ]
    search_fields = ["courseTitle"]
    ordering = ["id"]
    filter_horizontal = []

# Register the enrollment model
admin.site.register(Enrollment,EnrollmentAdmin)
