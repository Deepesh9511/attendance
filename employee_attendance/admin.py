from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdminHOD, Staffs, Courses, Subjects, Employees, Attendance, AttendanceReport, LeaveReportEmployee, LeaveReportStaff, FeedBackEmployee, FeedBackStaffs, NotificationEmployee, NotificationStaffs

# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHOD)
admin.site.register(Staffs)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(Employees)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportEmployee)
admin.site.register(LeaveReportStaff)
admin.site.register(FeedBackEmployee)
admin.site.register(FeedBackStaffs)
admin.site.register(NotificationEmployee)
admin.site.register(NotificationStaffs)
