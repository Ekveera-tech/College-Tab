from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import teacher,student,subject,teacher_assign,student_submission,assignment,Class,Test,student_testsubmission
from django.contrib import auth
from django.shortcuts import redirect,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import StudentForm
from .forms import TeacherForm,UserForm,AssignCreateForm,AssignSubmitForm,TestCreateForm
from django.urls import reverse
import datetime
#from PIL import Image
#import io
#from .. import web_socket

# Create your views here.
def index(request):
    template = loader.get_template('index.html')# change to index.html
    teachers = teacher_assign.objects.all()
    st = student.objects.all()
    subjects = subject.objects.all()
    tests = Test.objects.all()
    print(tests)
    context = {"teachers":teachers,"student":st,"sub":subjects,'Test':tests}
    return HttpResponse(template.render(context, request))




def exit_test(request):
    template = loader.get_template('test_exit.html')
    message = "Sorry, you can't take test in normal screen."
    context={"message":message}
    return HttpResponse(template.render(context,request))


#teacher views
def teacher_login(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            tobj = teacher.objects.get(user=user)
            #print(id,username,password)
            #return HttpResponseRedirect('/t_dashboard/%d/' % tobj.id)
            url = reverse('teacher:t_db', kwargs={'id': tobj.id})
            return HttpResponseRedirect(url)
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('/t_login')
    else:
        #form = TeacherForm()
        context = {}
        template = loader.get_template('teacher login.html')
        return HttpResponse(template.render(context, request))


def teacher_signup(request):
    if request.method == 'POST':
        uform = UserForm(request.POST)
        form = TeacherForm(request.POST)
        if uform.is_valid():
            user = uform.save()
            if form.is_valid():
                new_teacher = form.save(commit=False)
                new_teacher.user = user
                new_teacher.save()
                print(new_teacher)
    form = TeacherForm()
    uform = UserForm()
    context = {'form': form,'uform':uform}
    template = loader.get_template('teacher signup.html')
    return HttpResponse(template.render(context, request))




@login_required(login_url='t_login/')
def teacher_dashboard(request,id):
    template = loader.get_template('teachers dashboard.html')
    current_teacher = teacher.objects.get(id=id)
    assigned_classes = get_classes(current_teacher)
    context = {'teacher':current_teacher,'class_list':assigned_classes}
    return HttpResponse(template.render(context, request))


@login_required(login_url='t_login/')
def teacher_subject_assign(request, id, sub_id,class_id):           # to list assignements given subject and class
    if request.method == 'POST':
        form = AssignCreateForm(request.POST,request.FILES)
        if form.is_valid():
            new_assignment = form.save(commit=False)
            new_assignment.t_id = teacher.objects.get(id=id)
            new_assignment.c_id = Class.objects.get(id=class_id)
            new_assignment.s_id = subject.objects.get(subject_code=sub_id)
            new_assignment.save()
            print(new_assignment)
    form = AssignCreateForm()
    template = loader.get_template('teacher dashboard assignments.html')
    print(id,sub_id,class_id)
    current_teacher = teacher.objects.get(id=id)
    current_subject = subject.objects.get(subject_code=sub_id)
    current_class=Class.objects.get(id=class_id)
    assignment_list = get_assignment_teacher(current_subject,current_teacher)
    context = {'teacher':current_teacher,'assignment_list':assignment_list,'subject':current_subject,'class':current_class,'form':form}
    return HttpResponse(template.render(context, request))


#submission for test
@login_required(login_url='t_login/')
def teacher_assignment_submission(request,id,sub_id,class_id,a_id):# list students who have submitted this assignment
    current_teacher = teacher.objects.get(id=id)
    current_subject = subject.objects.get(subject_code=sub_id)
    current_class=Class.objects.get(id=class_id)
    template = loader.get_template('teacher_dashboard_assignment_submissions.html')
    a = assignment.objects.filter(id=a_id)
    student_submission_list = student_submission.objects.filter(a_id=a_id)
    all_students = student.objects.all().filter(branch=current_class.branch)
    student_who_submit = [s.stud_id for s in student_submission_list]
    context = {'submission_list':student_submission_list,'assignment':a,'subject':current_subject,'class':current_class,'teacher':current_teacher,'all_students':all_students,'student_who_submit':student_who_submit}
    return HttpResponse(template.render(context, request))

@login_required(login_url='t_login/')
def assignment_viewer(request,id):
    submission = student_submission.objects.filter(id=id)
    template = loader.get_template('index.html')
    context = {'submission':submission}
    return HttpResponse(template.render(context,request))


#Exam Create
def teach_exam_create(request,t_id,c_id,sub_id):
    current_teacher = teacher.objects.get(id=t_id)
    current_subject = subject.objects.get(subject_code=sub_id)
    current_class=Class.objects.get(id=c_id)
    exam_list = get_exam_teacher(current_subject,current_teacher,current_class)
    if request.method == 'POST':
        form = TestCreateForm(request.POST)
        if form.is_valid():
            new_test = form.save(commit=False)
            new_test.t_id = current_teacher
            new_test.c_id = current_class
            new_test.s_id = current_subject
            new_test.save()
            print(new_test)
    form = TestCreateForm()
    context = {'teacher':current_teacher,'exam_list':exam_list,'subject':current_subject,'class':current_class,'form':form}
    template = loader.get_template('teacher dashboard examination.html')
    return HttpResponse(template.render(context, request))

#test attempted
@login_required(login_url='t_login/')#list students who have given test and their report
def teacher_test_submission(request,t_id,c_id,sub_id,test_id):# list students who have submitted this assignment
    current_teacher = teacher.objects.get(id=t_id)
    current_subject = subject.objects.get(subject_code=sub_id)
    current_class=Class.objects.get(id=c_id)
    current_test = Test.objects.get(id=test_id)
    template = loader.get_template('teacher dashboard test submitted.html')
    student_submission_list = student_testsubmission.objects.filter(id=test_id)
    all_students = student.objects.all().filter(sem=current_class.sem).filter(sec=current_class.sec).filter(branch=current_class.branch)
    context = {'teacher':current_teacher,'student_submission_list':student_submission_list,'all_students':all_students,'subject':current_subject,'class':current_class,'test':current_test}
    return HttpResponse(template.render(context, request))


def t_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/t_login')




#student views
def student_login(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print(username,password)
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            print("correct")
            auth.login(request,user)
            stud = student.objects.get(user=user)
            return HttpResponseRedirect('/s_dashboard/%s/' % stud.enrollment_number)
            #url = reverse('t_dash', kwargs={'id': id})
            #return HttpResponseRedirect(url)
        else:
            print("wrong")
            messages.info(request,"Invalid Credentials")
            return redirect('/s_login')
    else:
        context = {}
        template = loader.get_template('student login.html')
        return HttpResponse(template.render(context, request))


def student_signup(request):
    if request.method == 'POST':
        uform = UserForm(request.POST)
        form = StudentForm(request.POST)
        if uform.is_valid():
            user = uform.save()
            if form.is_valid():
                new_student = form.save(commit=False)
                new_student.user = user
                new_student.save()
                print(new_student)
    form = StudentForm()
    uform = UserForm()
    context = {'form': form,'uform':uform}
    template = loader.get_template('student signup.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='s_login/')
def student_dashboard(request,id):
    template = loader.get_template('student dashboard.html')
    print(id)
    current_student = student.objects.get(enrollment_number=id)
    subjects = get_subjects(current_student)
    tests=get_tests(current_student)
    print(tests)
    now=current_datetime()
    if tests:
        context = {'student':current_student,'subject_list':subjects,'tests':tests,'error':'','cur_date':now}
        return HttpResponse(template.render(context, request))
    error='No tests assigned yet.'
    context = {'student':current_student,'subject_list':subjects,'error':error,'cur_date':now}
    return HttpResponse(template.render(context, request))


@login_required(login_url='s_login/')
def student_subject_assign(request,id,sub_id):           # to list assignements given subject and class
    template = loader.get_template('student_dashboard_subject_assignments.html')
    current_student = student.objects.get(enrollment_number=id)
    current_subject = subject.objects.get(subject_code=sub_id)
    assignment = get_assignments(current_student,current_subject)
    if assignment:
         context = {'student':current_student,'assignment_list':assignment,'subject':current_subject,'error':''}
    else:
        error="No teacher is assigned for this subject yet."
        context={'error':error,'student':current_student,'subject':current_subject}
    return HttpResponse(template.render(context, request))


@login_required(login_url='s_login/')
def stud_assign_submit(request,id,assign_id):
    current_student = student.objects.get(enrollment_number=id)
    assignment_current = assignment.objects.get(id=assign_id)
    if request.method=="POST":
        form = AssignSubmitForm(request.POST,request.FILES)
        print(form.is_valid(),form.data,request.FILES)
        if form.is_valid():
            new_submission = form.save(commit=False)
            new_submission.stud_id = current_student
            new_submission.a_id = assignment_current
            new_submission.save()
            print(new_submission,'successful submission!')
    template = loader.get_template('student_dashboard_assignment_upload.html')
    form = AssignSubmitForm()
    context = {'student':current_student,'assignment':assignment_current,'form':form}
    return HttpResponse(template.render(context, request))

@login_required(login_url='s_login/')
def stud_assign_download(request,id,assign_id):
    filename=get_assign_file(assign_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response

def stud_test(request,stud_id,test_id):
    template = loader.get_template('test.html')
    test = Test.objects.get(id=test_id)
    st = student.objects.get(enrollment_number=stud_id)
    print(test)
    context = {"student":st,'test':test}
    return HttpResponse(template.render(context, request))


@login_required(login_url='s_login/')
def s_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/s_login')



#Helper functions
def get_subjects(student):
    branch = student.branch
    sem = student.sem
    return subject.objects.filter(branch=branch).filter(sem=sem)


def get_classes(teacher):
    return teacher_assign.objects.filter(t_id=teacher)

def get_tests(student):
    try:
        curr_class = Class.objects.get(sem=student.sem,sec=student.sec,branch=student.branch)
        return Test.objects.filter(c_id=curr_class)
    except Test.DoesNotExist:
        return False

def get_assignments(student,subject):
    sem = student.sem
    sec = student.sec
    try:
        curr_class = Class.objects.filter(sem=sem).get(sec=sec)
        curr_teacher = teacher_assign.objects.filter(c_id=curr_class).get(s_id=subject)
        return assignment.objects.filter(c_id=curr_class).filter(s_id=subject)
    except assignment.DoesNotExist:
        return 'No assignments'.list()
    except teacher_assign.DoesNotExist:
        return False

def get_assignment_teacher(current_subject,current_teacher):
    try:
        return assignment.objects.filter(t_id=current_teacher).filter(s_id=current_subject)
    except teacher_assign.DoesNotExist:
        return False

def get_exam_teacher(current_subject,current_teacher,current_class):
    try:
        return Test.objects.filter(t_id=current_teacher).filter(s_id=current_subject).filter(c_id=current_class)
    except teacher_assign.DoesNotExist:
        return False

def current_datetime():
    now = datetime.datetime.now()
    return now

def get_assign_file(assign_id):
    path=assignment.objects.filter(assign_id=assign_id)
    return path.assignFile

def sortsub(l):
    return l['']

# def get_status(student,assignement):
#     try:
#         a_id=assignment.objects.get(c_id=assignment.c_id,s_id=assignment.s_id,topic=assignment.topic)
#         stud_id=student.objects.get(enrollment_number=student.enrollment_number,name=student.name)
#         stud_sub=student_submission.objects.get(a_id=a_id,stud_id=stud_id)
#         print("Got it")
#         return ''
#     except student_submission.DoesNotExist:
#         return 'Not submitted'



