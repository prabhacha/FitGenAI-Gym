from rest_framework import serializers
from .models import Workout, MembershipPlan
class WorkoutSerializer(serializers.ModelSerializer):
    class Meta: model=Workout; fields="__all__"
class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta: model=MembershipPlan; fields="__all__"
