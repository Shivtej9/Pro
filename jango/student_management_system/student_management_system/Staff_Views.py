from django.shortcuts import render,redirect
from app.models import Staff,Staff_Notification,Staff_Leave,Staff_Feedback,Subject,Session_Year,Student,Attendance,Attendance_Report,StudentResult
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def HOME(request):
    return render(request,'Staff/home.html')

@login_required(login_url='/')
def NOTIFICATIONS(request):
    staff=Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id
        notification = Staff_Notification.objects.filter(staff_id = staff_id)

        context={
            'notification':notification
        }
        return render(request,'Staff/notification.html',context)
@login_required(login_url='/')  
def STAFF_NOTIFICATION_MARK_AS_READ(request,status):
    notification = Staff_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('notifications')
@login_required(login_url='/')
def STAFF_APPLY_LEAVE(request):
    staff=Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id
        leave = Staff_Leave.objects.filter(staff_id = staff_id)
        context={
            'leave':leave
        }
        return render(request,'Staff/apply_leave.html',context)
    return render(request,'Staff/apply_leave.html')

@login_required(login_url='/')
def STAFF_APPLY_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_date=request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff = Staff.objects.get(admin = request.user.id)

        leave=Staff_Leave(
            staff_id = staff,
            date = leave_date,
            message = leave_message,
        )
        leave.save()
        messages.success(request,'Leave Applied Successfully !')
        return redirect('staff_apply_leave')
    return redirect('staff_apply_leave')

@login_required(login_url='/')
def STAFF_FEEDBACK(request):
    staff_id=Staff.objects.get(admin=request.user.id)
    
    feedback_history = Staff_Feedback.objects.filter(staff_id = staff_id)
    context={
        'feedback_history':feedback_history,
    }
    return render(request,'Staff/staff_feedback.html',context)


@login_required(login_url='/')
def STAFF_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        # feedback_reply = request.POST.get('feedback_reply')
        staff = Staff.objects.get(admin = request.user.id)
        feedback = Staff_Feedback(
            staff_id = staff,
            feedback = feedback,
            feedback_reply ="",
        )
        feedback.save()
        messages.success(request,'Feedback Sent Successfully !')
        return redirect('staff_feedback')
    
@login_required(login_url='/')
def STAFF_TAKE_ATTENDANCE(request):
    staff_id=Staff.objects.get(admin=request.user.id)
    subject=Subject.objects.filter(staff=staff_id)
    session_year=Session_Year.objects.all()
    action = request.GET.get('action')
    get_subject=None
    get_session_year=None
    students=None
    if action is not None:
        if request.method == "POST":
            
            subject_id=request.POST.get('subject_id')
            print(subject_id)
            session_year_id=request.POST.get('session_year_id')
            
            get_subject = Subject.objects.get(id = subject_id)
            get_session_year=Session_Year.objects.get(id=session_year_id)

            subject=Subject.objects.filter(id=subject_id)
            for i in subject:
                student_id=i.course.id
                students=Student.objects.filter(course_id=student_id)

    context={
        'subject':subject,
        'action':action,
        'session_year':session_year,
        'get_subject':get_subject,
        'get_session_year':get_session_year,
        'students':students

    }
    return render(request,'Staff/take_attendance.html',context)

def STAFF_TAKE_ATTENDANCE_SAVE(request):
    if request.method == "POST":
        subject_id=request.POST.get('subject_id')
        session_year_id=request.POST.get('session_year_id')
        attendance_date=request.POST.get('attendance_date')
        student_id=request.POST.getlist('student_id')

        get_subject=Subject.objects.get(id=subject_id)
        get_session_year=Session_Year.objects.get(id=session_year_id)

        attendance=Attendance(
            subject_id=get_subject,
            session_year_id=get_session_year,
            attendance_data=attendance_date,
        )
        attendance.save()
        for i in student_id:
            stud_id=i
            int_stud=int(stud_id)

            p_student=Student.objects.get(id=int_stud)
            attendance_report=Attendance_Report(
                student_id=p_student,
                attendance_id=attendance,
            )
            attendance_report.save()
    messages.success(request,"Data Saved Successfully")
    return redirect('staff_take_attendance')
    
def STAFF_VIEW_ATTENDANCE(request):
    staff_id=Staff.objects.get(admin=request.user.id)
    subject=Subject.objects.filter(staff_id=staff_id)
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
    return render(request,'Staff/view_attendance.html',context)

def STAFF_ADD_RESULT(request):
    staff = Staff.objects.get(admin = request.user.id)

    subjects = Subject.objects.filter(staff_id = staff)
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session = None
    students = None
    if action is not None:
        if request.method == "POST":
           subject_id = request.POST.get('subject_id')
           session_year_id = request.POST.get('session_year_id')

           get_subject = Subject.objects.get(id = subject_id)
           get_session = Session_Year.objects.get(id = session_year_id)

           subjects = Subject.objects.filter(id = subject_id)
           for i in subjects:
               student_id = i.course.id
               students = Student.objects.filter(course_id = student_id)


    context = {
        'subjects':subjects,
        'session_year':session_year,
        'action':action,
        'get_subject':get_subject,
        'get_session':get_session,
        'students':students,
    }

    return render(request,'Staff/add_result.html',context)


def STAFF_SAVE_RESULT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        assignment_mark = request.POST.get('assignment_mark')
        Exam_mark = request.POST.get('Exam_mark')

        get_student = Student.objects.get(admin = student_id)
        get_subject = Subject.objects.get(id=subject_id)

        check_exist = StudentResult.objects.filter(subject_id=get_subject, student_id=get_student).exists()
        if check_exist:
            result = StudentResult.objects.get(subject_id=get_subject, student_id=get_student)
            result.subject_assignment_marks = assignment_mark
            result.subject_exam_marks = Exam_mark
            result.save()
            messages.success(request, "Successfully Updated Result")
            return redirect('staff_add_result')
        else:
            result = StudentResult(student_id=get_student, subject_id=get_subject, exam_mark=Exam_mark,assignment_mark=assignment_mark)
            result.save()
            messages.success(request, "Successfully Added Result")
            return redirect('staff_add_result')