from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 
from app.models import Course,Session_Year,CustomUser,Student,Staff,Subject,Staff_Notification,Staff_Leave,Staff_Feedback,Student_Notification,Student_Feedback,Student_Leave,Attendance,Attendance_Report
from django.contrib import messages


@login_required(login_url='/')

def HOME(request):
    student_count=Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()
    student_gender_male=Student.objects.filter(gender = 'Male').count()
    student_gender_female=Student.objects.filter(gender = 'Female').count()
    # print(student_gender_male,student_gender_female)

    context={
        'student_count':student_count,
        'staff_count':staff_count,
        'course_count':course_count,
        'subject_count':subject_count,
        'student_gender_male':student_gender_male,
        'student_gender_female':student_gender_female,
    }

    return render(request,'Hod/home.html',context)

@login_required(login_url='/')
def ADD_STUDENT(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        # print(profile_pic)
        # print(first_name)
        # print(last_name)
        # print(email)
        # print(username)
        # print(password)
        # print(address)
        # print(gender)
        # print(course_id)
        # print(session_year_id)

        if CustomUser.objects.filter(email=email).exists():
           messages.warning(request,'Email Is Already Taken')
           return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
           messages.warning(request,'Username Is Already Taken')
           return redirect('add_student')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 3
            )
            user.set_password(password)
            user.save()

            course = Course.objects.get(id=course_id)
            session_year = Session_Year.objects.get(id=session_year_id)

            student = Student(
                admin = user,
                address = address,
                session_year_id = session_year,
                course_id = course,
                gender = gender,
            )
            student.save()
            messages.success(request, user.first_name + "  " + user.last_name + " is Successfully Added !")
            return redirect('add_student')

    context = {
        'course':course,
        'session_year':session_year,
    }

    return render(request,'Hod/add_student.html',context)


@login_required(login_url='/')
def VIEW_STUDENT(request):
    student = Student.objects.all()

    context = {
        'student':student,
    }
    return render(request,'Hod/view_student.html',context)

@login_required(login_url='/')
def EDIT_STUDENT(request,id):
    student = Student.objects.filter(id = id)
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    context = {
        'student':student,
        'course':course,
        'session_year':session_year,
    }
    return render(request,'Hod/edit_student.html',context)

@login_required(login_url='/')
def UPDATE_STUDENT(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        print(student_id)
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        user = CustomUser.objects.get(id = student_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        student = Student.objects.get(admin = student_id)
        student.address = address
        student.gender = gender

        course = Course.objects.get(id = course_id)
        student.course_id = course

        session_year = Session_Year.objects.get(id = session_year_id)
        student.session_year_id = session_year

        student.save()
        messages.success(request,'Record Are Successfully Updated !')
        return redirect('view_student')

    return render(request,'Hod/edit_student.html')

@login_required(login_url='/')
def DELETE_STUDENT(request,admin):
    student = CustomUser.objects.get(id = admin)
    student.delete()
    messages.success(request,'Record Are Successfully Deleted !')
    return redirect('view_student')

@login_required(login_url='/')
def ADD_COURSE(request):

    if request.method == "POST":
        course_name = request.POST.get('course_name')

        course = Course(
            name = course_name,
        )
        course.save()
        messages.success(request,'Course Are Successfully Created ')

        # engine.say("course are successfully added")

        # engine.runAndWait()
        # engine.endLoop()
        return redirect('view_course')

    return render(request,'Hod/add_course.html')

@login_required(login_url='/')
def VIEW_COURSE(request):
    course = Course.objects.all()
    context = {
        'course':course,
    }
    return render(request,'Hod/view_course.html',context)

@login_required(login_url='/')
def EDIT_COURSE(request,id):
    course = Course.objects.get(id = id)
    context={
        'course':course,
    }
    return render(request,'Hod/edit_course.html',context)

def UPDATE_COURSE(request):
    if request.method=="POST":
        name=request.POST.get('name')
        course_id=request.POST.get('course_id')
        course=Course.objects.get(id=course_id)
        course.name=name
        course.save()
        messages.success(request,"COURSE UPDATED !!")
        return redirect('view_course')

    return render(request,'Hod/edit_course.html')

@login_required(login_url='/')
def DELETE_COURSE(request,id):
    course = Course.objects.get(id = id)
    course.delete()
    messages.success(request,'Course are Successfully Deleted')

    return redirect('view_course')


@login_required(login_url='/')
def ADD_STAFF(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        # print(profile_pic,first_name,last_name,email,username,password,address,gender)
        if CustomUser.objects.filter(email=email).exists():
           messages.warning(request,'Email Is Already Taken')
           return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
           messages.warning(request,'Username Is Already Taken')
           return redirect('add_staff')
        
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 2
            )
            user.set_password(password)
            user.save()
            staff = Staff(
                admin = user,
                address = address,
                gender = gender,
            )
            staff.save()
            messages.success(request, user.first_name + "  " + user.last_name + " is Successfully Added !")
            return redirect('add_staff')

    return render(request,'Hod/add_staff.html')

@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()
    context={
        'staff':staff,
    }
    return render(request,'Hod/view_staff.html',context)

@login_required(login_url='/')
def EDIT_STAFF(request,id):
    staff = Staff.objects.get(id = id)
    context={
        'staff':staff,
    }
    return render(request,'Hod/edit_staff.html',context)

@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        try:
            user = CustomUser.objects.get(id = staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            if password != None and password != "":
                user.set_password(password)
            if profile_pic != None and profile_pic != "":
                user.profile_pic = profile_pic
            user.save()
            staff = Staff.objects.get(admin = staff_id)
            staff.address = address
            staff.gender = gender
            staff.save()
            messages.success(request,'Record Are Successfully Updated !')
            return redirect('view_staff')
        except:
            messages.error(request,'Failed To Update Record !')
            return redirect('view_staff')
    else:
        messages.warning(request,"Please Fill All The Fields")
        return redirect('view_staff') 
    return render(request,'Hod/edit_staff.html')

@login_required(login_url='/')
def DELETE_STAFF(request,id):
    staff = CustomUser.objects.get(id = id)
    staff.delete()
    messages.success(request,'Record Are Successfully Deleted !')
    return redirect('view_staff')

@login_required(login_url='/')
def ADD_SUBJECT(request):
    course = Course.objects.all()
    staff = Staff.objects.all() 
    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')
        course = Course.objects.get(id = course_id)
        staff = Staff.objects.get(id = staff_id)
        subject = Subject(
            name = subject_name,
            course = course,
            staff = staff,
        )
        subject.save()
        messages.success(request,'Subject Are Successfully Added !')
        return redirect('add_subject')
    context={
        'course':course,
        'staff':staff,
    }
    
    return render(request,'Hod/add_subject.html',context)

@login_required(login_url='/')
def VIEW_SUBJECT(request):
    subject = Subject.objects.all()
    context={
        'subject':subject,
    }
    return render(request,'Hod/view_subject.html',context)

@login_required(login_url='/')
def EDIT_SUBJECT(request,id):
    subject = Subject.objects.get(id = id)
    course = Course.objects.all()
    staff = Staff.objects.all()
    context={
        'subject':subject,
        'course':course,
        'staff':staff,
    }
    return render(request,'Hod/edit_subject.html',context)

@login_required(login_url='/')
def UPDATE_SUBJECT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')
        course = Course.objects.get(id = course_id)
        staff = Staff.objects.get(id = staff_id)
        subject = Subject.objects.get(id = subject_id)
        subject.name = subject_name
        subject.course = course
        subject.staff = staff
        subject.save()
        messages.success(request,'Subject Are Successfully Updated !')
        return redirect('view_subject')
    else:
        messages.warning(request,"Please Fill All The Fields")
        return redirect('view_subject') 
    return render(request,'Hod/edit_subject.html')
@login_required(login_url='/')
def DELETE_SUBJECT(request,id):
    subject = Subject.objects.get(id = id)
    subject.delete()
    messages.success(request,'Record Are Successfully Deleted !')
    return redirect('view_subject')


@login_required(login_url='/')
def ADD_SESSION(request):
    if request.method == "POST":
        session_start_year = request.POST.get('session_year_start')
        session_end_year = request.POST.get('session_year_end')
        session = Session_Year(
            session_start = session_start_year,
            session_end = session_end_year,
        )
        session.save()
        messages.success(request,'Session Are Successfully Added !')
        return redirect('add_session')
    return render(request,'Hod/add_session.html')

@login_required(login_url='/')
def VIEW_SESSION(request):
    session = Session_Year.objects.all()
    context={
        'session':session,
    }
    return render(request,'Hod/view_session.html',context)

@login_required(login_url='/')
def EDIT_SESSION(request,id):
    session = Session_Year.objects.filter(id = id)
    context={
        'session':session,
    }
    return render(request,'Hod/edit_session.html',context)

@login_required(login_url='/')
def UPDATE_SESSION(request):
    if request.method == "POST":
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_year_start')
        session_end_year = request.POST.get('session_year_end')
        session = Session_Year.objects.get(id = session_id)
        session.session_start = session_start_year
        session.session_end = session_end_year
        session.save()
        messages.success(request,'Session Are Successfully Updated !')
        return redirect('view_session')
    else:
        messages.warning(request,"Please Fill All The Fields")
        return redirect('view_session') 
    return render(request,'Hod/edit_session.html')
    
    

@login_required(login_url='/')
def DELETE_SESSION(request,id):
    session = Session_Year.objects.get(id = id)
    session.delete()
    messages.success(request,'Record Are Successfully Deleted !')
    return redirect('view_session')

@login_required(login_url='/')
def STAFF_SEND_NOTIFICATION(request):
    staff = Staff.objects.all()
    see_notification=Staff_Notification.objects.all().order_by('-id')#[0:5]
    context={
        'staff':staff,
        'see_notification':see_notification,
    }
    return render(request,'Hod/staff_send_notification.html',context)

@login_required(login_url='/')
def SAVE_STAFF_NOTIFICATION(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')
        staff = Staff.objects.get(admin = staff_id)
        staff_notification = Staff_Notification(
            staff_id = staff,
            message = message,
        )
        staff_notification.save()
        messages.success(request,'Notification Are Successfully Sent !')
        return redirect('staff_send_notification')

@login_required(login_url='/')
def STAFF_LEAVE_VIEW(request):
    staff = Staff.objects.all()
    staff_leave=Staff_Leave.objects.all().order_by('-id')
    context={
        'staff':staff,
        'staff_leave':staff_leave,
    }
    return render(request,'Hod/staff_leave.html',context)

@login_required(login_url='/')
def STAFF_APPROVE_LEAVE(request,id):
    leave=Staff_Leave.objects.get(id = id)
    leave.status = 1
    leave.save()
    messages.success(request,'Leave Are Successfully Approved !')
    return redirect('staff_leave_view')

@login_required(login_url='/')
def STAFF_DISAPPROVE_LEAVE(request,id):
    leave=Staff_Leave.objects.get(id = id)
    leave.status = 2
    leave.save()
    messages.success(request,'Leave Are Successfully Disapproved !')
    return redirect('staff_leave_view')

@login_required(login_url='/')
def STAFF_FEEDBACK(request):
    feedback= Staff_Feedback.objects.all()
    context={
        'feedback':feedback,
    }
    return render(request,'Hod/staff_feedback.html',context)

@login_required(login_url='/')
def STAFF_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback_id=request.POST.get('feedback_id')
        feedback_reply=request.POST.get('feedback_reply')
        feedback=Staff_Feedback.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_reply
        feedback.save()
        messages.success(request,'Feedback Are Successfully Sent !')
        return redirect('staff_feedback_reply')
    
@login_required(login_url='/')
def STUDENT_SEND_NOTIFICATION(request):
    student = Student.objects.all()
    see_notification=Student_Notification.objects.all().order_by('-id')#[0:5]
    context={
        'student':student,
        'see_notification':see_notification,
    }
    return render(request,'Hod/student_send_notification.html',context)

@login_required(login_url='/')
def SAVE_STUDENT_NOTIFICATION(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        message = request.POST.get('message')
        student = Student.objects.get(admin = student_id)
        student_notification = Student_Notification(
            student_id = student,
            message = message,
        )
        student_notification.save()
        messages.success(request,'Notification Are Successfully Sent !')
        return redirect('student_send_notification')
    
def STUDENT_FEEDBACK(request):
    feedback= Student_Feedback.objects.all()
    feedback_history= Student_Feedback.objects.all().order_by('-id')[0:5]
    context={
        'feedback':feedback,
        'feedback_history':feedback_history,
    }
    return render(request,'Hod/student_feedback.html',context)

def STUDENT_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback_id=request.POST.get('feedback_id')
        feedback_reply=request.POST.get('feedback_reply')
        feedback=Student_Feedback.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_reply
        feedback.status=1
        feedback.save()
        messages.success(request,'Feedback Reply Sent Successfully !')
        return redirect('student_feedback_reply')
    
def STUDENT_LEAVE_VIEW(request):
    student = Student.objects.all()
    student_leave=Student_Leave.objects.all().order_by('-id')
    context={
        'student':student,
        'student_leave':student_leave,
    }
    return render(request,'Hod/student_leave.html',context)

def STUDENT_APPROVE_LEAVE(request,id):
    leave=Student_Leave.objects.get(id = id)
    leave.status = 1
    leave.save()
    messages.success(request,'Leave Are Successfully Approved !')
    return redirect('student_leave_view')

def STUDENT_DISAPPROVE_LEAVE(request,id):
    leave=Student_Leave.objects.get(id = id)
    leave.status = 2
    leave.save()
    messages.success(request,'Leave Are Successfully Disapproved !')
    return redirect('student_leave_view')
def HOD_VIEW_ATTENDANCE(request):
    subject=Subject.objects.all()
    session_year=Session_Year.objects.all()
    action = request.GET.get('action')
    get_subject=None
    get_session_year=None
    attendance_date=None
    attendance_report=None
    if action is not None:
        if request.method == "POST":
            
            subject_id=request.POST.get('subject_id')
            attendance_date=request.POST.get('attendance_date')
            session_year_id=request.POST.get('session_year_id')
            
            get_subject = Subject.objects.get(id = subject_id)
            get_session_year=Session_Year.objects.get(id=session_year_id)
            
            attendance=Attendance.objects.filter(subject_id=get_subject,attendance_data=attendance_date)
            for i in attendance:
                attendance_id=i.id
                attendance_report=Attendance_Report.objects.filter(attendance_id=attendance_id)
                
    context={
        'subject':subject,
        'action':action,
        'session_year':session_year,
        'get_subject':get_subject,
        'attendance_data':attendance_date,
        'get_session_year':get_session_year,
        'attendance_report':attendance_report,

    }
    return render(request,'Hod/hod_view_attendance.html',context)