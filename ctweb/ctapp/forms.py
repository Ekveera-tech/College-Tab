from django.db.models.enums import Choices
from django.forms import ModelForm
from .models import student
from .models import teacher,assignment,student_submission,Test,student_testsubmission
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

SEMESTER_CHOICES = [("1", 1),("2", 2),("3", 3),("4", 4),("5", 5),("6", 6),("7", 7),("8", 8),]
BRANCH_CHOICES = [("IT","IT"),("CS", "CS"),("EC", "EC"),("MECH", "MECH"),("EE", "EE"),("EX", "EX"),("CIVIL", "CIVIL"),]
SEC_CHOICES = [('A','A'),('B','B'),('C','C')]
CLG_CHOICES = [('LNCT','LNCT'),('LNCTS','LNCTS'),('LNCTE','LNCTE')]

class StudentForm(ModelForm):
    class Meta:
        model = student
        fields = ["enrollment_number", "name", "college_name", "email", 'sem', 'sec','branch','mobile_no']
 

class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['username'].help_text=' '
      self.fields['password1'].help_text=' '
      self.fields['password2'].help_text=' '
    class Meta:
        model = User
        fields = ('username','password1', 'password2')
        

class TeacherForm(ModelForm):
    class Meta:
        model = teacher
        fields = ["name", "college_name", "email", 'branch','mobile_no']
        


class AssignSubmitForm(ModelForm):
    class Meta:
        model = student_submission
        fields = ["file"]


class AssignCreateForm(ModelForm):
    class Meta:
        model = assignment
        fields = ["topic","last_date","assignfile"]


class TestCreateForm(ModelForm):
    class Meta:
        model = Test
        fields = ["topic","form_link","link","date","starttime","endtime"]




