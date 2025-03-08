from rest_framework import serializers
from .models import Subject, Custodian, Alarm

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class CustodianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custodian
        fields = '__all__'

class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = '__all__'