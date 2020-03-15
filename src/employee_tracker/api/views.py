from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Attendant, Vacation, Leave
from .serializers import Attendanterializer, VacationSerializer, LeaveSerializer
from datetime import datetime, timedelta


def subtract_time(in_time, out_time) -> datetime:
    tIn = timedelta(hours=in_time.hour, minutes=out_time.minute)
    return out_time - tIn


class EmployeeProcess:
    @staticmethod
    def prepare_attendant_list_for_one_employee(list_attendant):
        list = [x for x in list_attendant.values('in_time', 'out_time')]
        out_time = ""
        for i in range(len(list)):
            if list[i]['out_time'] is not None:
                out_time = list[i]['out_time']
            else:
                if out_time != "":
                    list[i]['out_time'] = out_time
                else:
                    list[i]['out_time'] = list[i]['in_time'].__add__(timedelta(hours=8))
        return list

    @staticmethod
    def working_hours(list_attendant):
        return sum([subtract_time(attendant['in_time'], attendant['out_time']).hour for attendant in list_attendant])

    @staticmethod
    def leaving_hours(list_leaving):
        return sum([subtract_time(leaving['in_time'], leaving['out_time']).hour for leaving in list_leaving])


class EmployeeWorkingHours(GenericAPIView, EmployeeProcess):
    def get(self, request, *args, **kwargs):
        type = kwargs.get('t')

        try:
            if type == 'w':
                week_date_from_now = datetime.now().date() - timedelta(days=7)

                working_hours_employee = [self.print_working_hours(user, self.working_hours(
                    self.prepare_attendant_list_for_one_employee(user.attendant.filter(date__gte=week_date_from_now))),
                                                                   'weekly') for
                                          user
                                          in
                                          User.objects.all()]
                return Response(working_hours_employee)

            elif type == 'q':
                week_date_from_now = datetime.now().date() - timedelta(days=91)
                working_hours_employee = [self.print_working_hours(user, self.working_hours(
                    self.prepare_attendant_list_for_one_employee(user.attendant.filter(date__gte=week_date_from_now))),
                                                                   'quarter') for
                                          user in
                                          User.objects.all()]
                return Response(working_hours_employee)
            elif type == 'y':
                week_date_from_now = datetime.now().date() - timedelta(days=365)
                working_hours_employee = [self.print_working_hours(user, self.working_hours(
                    self.prepare_attendant_list_for_one_employee(user.attendant.filter(date__gte=week_date_from_now))),
                                                                   'yearly') for
                                          user
                                          in
                                          User.objects.all()]
                return Response(working_hours_employee)
            else:
                raise Exception("Determine the period")
        except Exception as ex:
            return Response(str(ex))

    @staticmethod
    def print_working_hours(employee, working_hours, period):
        return {"EmpName": employee.username, f"working hours {period}": working_hours}


class TeamComingToLeaving(GenericAPIView, EmployeeProcess):
    def get(self, request, *args, **kwargs):
        try:
            every_emp_with_working_hours = [
                self.working_hours(self.prepare_attendant_list_for_one_employee(user.attendant)) for user in
                User.objects.all()]
            every_emp_with_leaving_hours = [
                self.working_hours(self.prepare_attendant_list_for_one_employee(user.leaves)) for user in
                User.objects.all()]
            sum_work_hours = 0
            for working_hour in every_emp_with_working_hours:
                sum_work_hours += working_hour
            if sum_work_hours == 0:
                raise Exception("This Team has no work hour ")
            sum_leave_hours = 0
            for leaving_hour in every_emp_with_leaving_hours:
                sum_leave_hours += leaving_hour
            return Response(f"this team has an leaving of percent {sum_leave_hours // sum_work_hours} %")

        except Exception as ex:
            return Response(str(ex))


class AttendantEmployeeCreateView(GenericAPIView):
    serializer_class = Attendanterializer
    queryset = Attendant.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        emp_id = kwargs.get('employee_Id')
        try:
            user = User.objects.filter(pk=emp_id).exists()
            if not user:
                raise Exception("User dose't exist")
            attend = Attendant.objects.filter(Q(emp_id=emp_id) & Q(date=datetime.now().date()))
            if attend.count() == 0:
                newAttendant = self.serializer_class(data={'emp': emp_id})
                newAttendant.is_valid(raise_exception=True)
                newAttendant.save()
                return Response({'message:Thank you'})

            elif attend.first().out_time is None:
                clone_attendant: Attendant = attend.first()
                clone_attendant.out_time = datetime.now()
                clone_attendant.save()
                return Response({'message:Thank you'})
        except Exception as e:
            return Response({'error': str(e)})


class CreateEmployeeVacation(CreateAPIView):
    serializer_class = VacationSerializer
    queryset = Vacation.objects.all()
    permission_classes = [IsAuthenticated]



class CreateLeaveEmployee(CreateAPIView):
    serializer_class = LeaveSerializer
    queryset = Leave.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        employee_Id = kwargs.get('employee_Id')
        try:
            user = User.objects.get(pk=employee_Id)
            if user is None:
                raise Exception("User dose't exist")
            leave = Leave.objects.filter(Q(emp_id=employee_Id) & Q(date=datetime.now().date()))
            if leave.count() == 0:
                newLeave = self.serializer_class(data={'emp': employee_Id})
                newLeave.is_valid(raise_exception=True)
                newLeave.save()
                return Response({'message:Thank you'})

            elif leave[0].out_time is None:
                cloneattend: Leave = leave.first()
                cloneattend.out_time = datetime.now()
                cloneattend.save()
                return Response({'message:Thank you'})
        except Exception as e:
            return Response({'error': str(e)})
