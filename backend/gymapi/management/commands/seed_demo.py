from django.core.management.base import BaseCommand
from gymapi.models import Workout, MembershipPlan

class Command(BaseCommand):
    help = "Create sample gym workouts and membership plans if the tables are empty."
    def handle(self, *args, **options):
        if not Workout.objects.exists():
            Workout.objects.bulk_create([
                Workout(title="Full Body Strength", category="Strength", duration_minutes=45, level="Beginner", description="A balanced full-body session with controlled movements.", is_featured=True),
                Workout(title="Cardio Starter", category="Cardio", duration_minutes=25, level="Beginner", description="Easy-paced cardio with warm-up and cool-down."),
                Workout(title="Upper Body Builder", category="Strength", duration_minutes=40, level="Intermediate", description="A push-and-pull upper-body session."),
                Workout(title="Mobility Reset", category="Mobility", duration_minutes=20, level="All levels", description="Gentle mobility and stretching session."),
            ])
            self.stdout.write(self.style.SUCCESS("Sample workouts created."))
        if not MembershipPlan.objects.exists():
            MembershipPlan.objects.bulk_create([
                MembershipPlan(name="Starter", price_inr=999, duration="1 month", description="A simple monthly gym plan.", features=["Gym access", "Fitness orientation"]),
                MembershipPlan(name="Pro", price_inr=2499, duration="3 months", description="Build consistency with more support.", features=["Gym access", "Trainer consultation", "Progress review"]),
                MembershipPlan(name="Elite", price_inr=7999, duration="12 months", description="A yearly membership option.", features=["Gym access", "Trainer consultation", "Monthly progress review"]),
            ])
            self.stdout.write(self.style.SUCCESS("Sample membership plans created."))
