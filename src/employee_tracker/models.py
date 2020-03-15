from django.db import models
from django.contrib.auth.models import User


class BaseAttendanceLeave(models.Model):
    in_time = models.DateTimeField(auto_now=True, editable=True)
    out_time = models.DateTimeField(null=True, blank=True)
    date = models.DateField(auto_now_add=True, editable=True)

    class Meta:
        abstract = True


class Attendant(BaseAttendanceLeave):
    emp = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="attendant")


class Vacation(models.Model):
    emp = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="vacations")
    date = models.DateField()

    class Meta:
        unique_together = [['emp', 'date']]


class Leave(BaseAttendanceLeave):
    emp = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="leaves")
