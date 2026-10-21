from django.urls import path
from . import views
urlpatterns=[path("health/",views.health),path("workouts/",views.workouts),path("plans/",views.plans),path("ai/coach/",views.ai_coach)]
