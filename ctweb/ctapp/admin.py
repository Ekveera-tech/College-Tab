from django.contrib import admin
from django.apps import apps
from .models import student,subject,student_submission,teacher,teacher_assign,assignment,Class,Test,student_testsubmission

# Register your models here.
admin.site.register(subject)
admin.site.register(student_submission)
admin.site.register(student)
admin.site.register(Class)
admin.site.register(assignment)
admin.site.register(teacher_assign)
admin.site.register(teacher)
admin.site.register(Test)
admin.site.register(student_testsubmission)








