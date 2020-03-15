from rest_framework import serializers
from ..models import Attendant, Vacation, Leave


class Attendanterializer(serializers.ModelSerializer):
    class Meta:
        model = Attendant
        fields = '__all__'


class VacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = '__all__'


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'
