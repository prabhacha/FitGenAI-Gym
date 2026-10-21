from django.db import models
class Workout(models.Model):
    title=models.CharField(max_length=120)
    category=models.CharField(max_length=30,default="Strength")
    duration_minutes=models.PositiveIntegerField(default=30)
    level=models.CharField(max_length=30,default="Beginner")
    description=models.TextField()
    is_featured=models.BooleanField(default=False)
    def __str__(self): return self.title
class MembershipPlan(models.Model):
    name=models.CharField(max_length=80)
    price_inr=models.PositiveIntegerField()
    duration=models.CharField(max_length=50)
    description=models.TextField()
    features=models.JSONField(default=list,blank=True)
    def __str__(self): return self.name
