import json
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Workout, MembershipPlan
from .serializers import WorkoutSerializer, MembershipPlanSerializer

DEFAULT_WORKOUTS=[
 {"id":1,"title":"Full Body Foundations","category":"Strength","duration_minutes":40,"level":"Beginner","description":"A balanced introduction to major movement patterns.","is_featured":True},
 {"id":2,"title":"Cardio Intervals","category":"Cardio","duration_minutes":25,"level":"Intermediate","description":"Moderate effort with comfortable recovery periods.","is_featured":True},
 {"id":3,"title":"Mobility Reset","category":"Mobility","duration_minutes":15,"level":"Beginner","description":"Gentle mobility for hips, shoulders and upper back.","is_featured":False},
 {"id":4,"title":"Core Stability","category":"Core","duration_minutes":20,"level":"Beginner","description":"Controlled exercises to develop trunk stability.","is_featured":False},
]
DEFAULT_PLANS=[
 {"id":1,"name":"Starter","price_inr":999,"duration":"1 month","description":"A simple way to build your routine.","features":["Gym floor access","Fitness orientation","Progress check-in"]},
 {"id":2,"name":"Performance","price_inr":2499,"duration":"3 months","description":"For consistent training and progress.","features":["Gym floor access","Group classes","Monthly progress review"]},
 {"id":3,"name":"Elite","price_inr":4999,"duration":"3 months","description":"Extra guidance to support your goals.","features":["All Performance features","Trainer consultation","Priority class booking"]},
]
@api_view(["GET"])
def health(request): return Response({"status":"ok","app":"FitGenAI Gym API"})
@api_view(["GET"])
def workouts(request):
    qs=Workout.objects.all().order_by("id")
    return Response(WorkoutSerializer(qs,many=True).data if qs.exists() else DEFAULT_WORKOUTS)
@api_view(["GET"])
def plans(request):
    qs=MembershipPlan.objects.all().order_by("price_inr")
    return Response(MembershipPlanSerializer(qs,many=True).data if qs.exists() else DEFAULT_PLANS)
def fallback(goal,level,days,equipment):
    gl=goal.lower()
    focus=("Prioritize progressive resistance training, sound technique, recovery and balanced meals." if ("strength" in gl or "muscle" in gl)
      else "Combine manageable strength sessions with low-impact cardio and sustainable habits." if ("weight" in gl or "fat" in gl)
      else "Build consistency with strength, cardio, mobility and adequate rest.")
    schedule=[
      {"day":"Day 1","session":"Full-body strength","details":"Squat variation, push movement, row, hip hinge and comfortable core work."},
      {"day":"Day 2","session":"Cardio + mobility","details":"20–30 minutes at a conversational pace, followed by gentle mobility."},
      {"day":"Day 3","session":"Strength technique","details":"Practice controlled movements with light-to-moderate effort."},
      {"day":"Day 4","session":"Active recovery","details":"Easy walking and gentle stretching, or rest if tired."},
      {"day":"Day 5","session":"Full-body strength","details":"Repeat familiar movements; progress only if technique feels comfortable."},
      {"day":"Day 6","session":"Optional enjoyable cardio","details":"Choose cycling, swimming, walking or another activity you enjoy."},
    ][:days]
    return {"source":"built-in-fallback","title":"Starter plan: "+goal,"summary":focus,"goal":goal,"level":level,
      "equipment":equipment,"days_per_week":days,"schedule":schedule,
      "habits":["Warm up for 5–10 minutes.","Increase workload gradually; stop if you feel sharp pain or unwell.","Prioritize sleep, hydration and balanced meals.","Take rest days and adapt sessions to your ability."],
      "disclaimer":"General fitness information only, not medical advice. Consult a qualified professional if you have health concerns."}
@api_view(["POST"])
def ai_coach(request):
    goal=str(request.data.get("goal","General fitness"))[:100]
    level=str(request.data.get("level","beginner"))[:30]
    equipment=str(request.data.get("equipment","Full gym"))[:80]
    try: days=max(1,min(6,int(request.data.get("days_per_week",3))))
    except (TypeError,ValueError): days=3
    backup=fallback(goal,level,days,equipment)
    if not settings.OPENAI_API_KEY: return Response(backup)
    try:
        from openai import OpenAI
        client=OpenAI(api_key=settings.OPENAI_API_KEY)
        prompt=("Create a conservative general fitness routine, not medical advice. Include rest and warm-up. "
        "Return JSON keys title,summary,goal,level,equipment,days_per_week,schedule (array of day,session,details),habits,disclaimer. "
        f"Goal={goal}; level={level}; days per week={days}; equipment={equipment}.")
        result=client.chat.completions.create(model=settings.OPENAI_MODEL,
          messages=[{"role":"system","content":"You are a cautious fitness planning assistant. Return JSON only."},
                    {"role":"user","content":prompt}],
          response_format={"type":"json_object"},temperature=0.4)
        data=json.loads(result.choices[0].message.content); data["source"]="openai"
        return Response(data)
    except Exception:
        return Response(backup)
