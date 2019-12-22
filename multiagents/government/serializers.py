from rest_framework import serializers
from .models import AgentsLog, Budget, RateList, AgentsState

class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgentsState
        fields = '__all__'

class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = '__all__'


class AgentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgentsLog
        fields = '__all__'


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RateList
        fields = '__all__'
