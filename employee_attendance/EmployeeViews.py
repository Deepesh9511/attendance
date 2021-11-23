from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
import datetime # To Parse input DateTime into Python Date Time Object

from employee_attendance.models import CustomUser, Staffs, Courses, Subjects, Employees, Attendance, AttendanceReport, LeaveReportEmployee, FeedBackEmployee, EmployeeResult


def employee_home(request):
    employee_obj = Employees.objects.get(admin=request.user.id)
    total_attendance = AttendanceReport.objects.filter(employee_id=employee_obj).count()
    attendance_present = AttendanceReport.objects.filter(employee_id=employee_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(employee_id=employee_obj, status=False).count()

    course_obj = Courses.objects.get(id=employee_obj.course_id.id)
    total_subjects = Subjects.objects.filter(course_id=course_obj).count()

    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subjects.objects.filter(course_id=employee_obj.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, employee_id=employee_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, employee_id=employee_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)
    
    context={
        "total_attendance": total_attendance,
        "attendance_present": attendance_present,
        "attendance_absent": attendance_absent,
        "total_subjects": total_subjects,
        "subject_name": subject_name,
        "data_present": data_present,
        "data_absent": data_absent
    }
    return render(request, "employee_template/employee_home_template.html", context)


def employee_view_attendance(request):
    employee = Employees.objects.get(admin=request.user.id) # Getting Logged in employee Data
    course = employee.course_id # Getting Course Enrolled of LoggedIn employee
    # course = Courses.objects.get(id=employee.course_id.id) # Getting Course Enrolled of LoggedIn employee
    subjects = Subjects.objects.filter(course_id=course) # Getting the Subjects of Course Enrolled
    context = {
        "subjects": subjects
    }
    return render(request, "employee_template/employee_view_attendance.html", context)


def employee_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('employee_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subjects.objects.get(id=subject_id)
        # Getting Logged In User Data
        user_obj = CustomUser.objects.get(id=request.user.id)
        # Getting employee Data Based on Logged in Data
        stud_obj = Employees.objects.get(admin=user_obj)
        # Now Accessing Attendance Data based on the Range of Date Selected and Subject Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse), subject_id=subject_obj)
        # Getting Attendance Report based on the attendance details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, employee_id=stud_obj)

        # for attendance_report in attendance_reports:
        #     print("Date: "+ str(attendance_report.attendance_id.attendance_date), "Status: "+ str(attendance_report.status))

        # messages.success(request, "Attendacne View Success")

        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports
        }

        return render(request, 'employee_template/employee_attendance_data.html', context)
       

def employee_apply_leave(request):
    employee_obj = Employees.objects.get(admin=request.user.id)
    leave_data = LeaveReportemployee.objects.filter(employee_id=employee_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'employee_template/employee_apply_leave.html', context)


def employee_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('employee_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        employee_obj = Employees.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportEmployee(employee_id=employee_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('employee_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('employee_apply_leave')


def employee_feedback(request):
    employee_obj = Employees.objects.get(admin=request.user.id)
    feedback_data = FeedBackemployee.objects.filter(employee_id=employee_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'employee_template/employee_feedback.html', context)


def employee_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('employee_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        employee_obj = Employees.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackEmployee(employee_id=employee_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('employee_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('employee_feedback')


def employee_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    employee = employees.objects.get(admin=user)

    context={
        "user": user,
        "employee": employee
    }
    return render(request, 'employee_template/employee_profile.html', context)


def employee_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('employee_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            employee = Employee.objects.get(admin=customuser.id)
            employee.address = address
            employee.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('employee_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('employee_profile')


def employee_view_result(request):
    employee = employees.objects.get(admin=request.user.id)
    employee_result = EmployeeResult.objects.filter(employee_id=employee.id)
    context = {
        "employee_result": employee_result,
    }
    return render(request, "employee_template/employee_view_result.html", context)





