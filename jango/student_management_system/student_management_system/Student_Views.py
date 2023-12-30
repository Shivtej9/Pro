from django.shortcuts import render,redirect
from app.models import Student,Student_Notification,Student_Feedback,Student_Leave,Attendance,Attendance_Report,Subject,Session_Year,StudentResult
from django.contrib.auth.decorators import login_required 
from django.contrib import messages


@login_required(login_url='/')
def HOME(request):
    return render(request,'Student/home.html')

@login_required(login_url='/')
def STUDENT_NOTIFICATIONS(request):
    student = Student.objects.filter(admin = request.user.id)
    for i in student:
        student_id=i.id
        notification=Student_Notification.objects.filter(student_id= student_id)
        context={
            'notification':notification,
        }
    
        return render(request,'Student/student_notifications.html',context)
    return render(request,'Student/student_notifications.html')

@login_required(login_url='/')
def STUDENT_NOTIFICATION_MARK_AS_READ(request,status):
    notification=Student_Notification.objects.get(id=status)
    notification.status=1
    notification.save()
    return redirect('student_notifications')

@login_required(login_url='/')
def STUDENT_FEEDBACK(request):
    student_id= Student.objects.get(admin = request.user.id)
    feedback_history=Student_Feedback.objects.filter(student_id=student_id).order_by('-id') 
    context={
        'feedback_history':feedback_history,
    }
    return render(request,'Student/student_feedback.html',context)

@login_required(login_url='/')
def STUDENT_FEEDBACK_SAVE(request):
    if request.method=='POST':
        student=Student.objects.get(admin = request.user.id)
        feedback=request.POST.get('feedback')
        feedbacks=Student_Feedback(
            student_id=student,
            feedback=feedback,
            feedback_reply= ""
        )
        feedbacks.save()
        messages.success(request,'Feedback Are Successfully Sent !')
        return redirect('student_feedback')
    
@login_required(login_url='/')
def STUDENT_APPLY_LEAVE(request):
    student = Student.objects.get(admin = request.user.id)
    leave = Student_Leave.objects.filter(student_id = student)
    context={
        'leave':leave
    }
    return render(request,'Student/student_apply_leave.html',context)

def STUDENT_APPLY_LEAVE_SAVE(request):
    if request.method=='POST':
        leave_date=request.POST.get('leave_date')
        leave_message=request.POST.get('leave_message')
        student_id=Student.objects.get(admin = request.user.id)
        leave=Student_Leave(
            student_id=student_id,
            message=leave_message,
            date=leave_date,
        )
        leave.save()
        messages.success(request,'Leave Are Successfully Applied !')
        return redirect('student_apply_leave')
    
def STUDENT_VIEW_ATTENDANCE(request):
    student = Student.objects.get(admin = request.user.id)
    subjects=Subject.objects.filter(course=student.course_id)
    action=request.GET.get('action')
    get_subject=None
    attendance_report=None
    if action is not None:
        if request.method == "POST":
            subject_id=request.POST.get('subject_id')
            get_subject = Subject.objects.get(id = subject_id)
            attendance_report=Attendance_Report.objects.filter(student_id=student,attendance_id__subject_id=subject_id)
    context={
        'subjects':subjects,
        'action':action,
        'get_subject':get_subject,
        'attendance_report':attendance_report,
    }
    return render(request,'Student/student_view_attendance.html',context)

def VIEW_RESULT(request):
    mark=None
    student=Student.objects.get(admin=request.user.id)
    result=StudentResult.objects.filter(student_id=student)
    for i in result:
        assignment_mark=i.assignment_mark
        exam_mark=i.exam_mark

        mark=assignment_mark+exam_mark

    context={
        'result':result,
        'mark':mark,
    }
    return render(request,'Student/view.html',context)
