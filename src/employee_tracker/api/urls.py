from django.urls import path
from .views import AttendantEmployeeCreateView, CreateEmployeeVacation, CreateLeaveEmployee, EmployeeWorkingHours, \
    TeamComingToLeaving

urlpatterns = [
    path('check/<int:employee_Id>', AttendantEmployeeCreateView.as_view()),
    path('vacation/', CreateEmployeeVacation.as_view()),
    path('leave/<int:employee_Id>', CreateLeaveEmployee.as_view()),
    path('workingHour/<str:t>', EmployeeWorkingHours.as_view()),
    path('teamComeToLeave', TeamComingToLeaving.as_view()),
]
