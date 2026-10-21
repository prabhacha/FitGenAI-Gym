from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="MembershipPlan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80)),
                ("price_inr", models.PositiveIntegerField()),
                ("duration", models.CharField(max_length=50)),
                ("description", models.TextField()),
                ("features", models.JSONField(blank=True, default=list)),
            ],
        ),
        migrations.CreateModel(
            name="Workout",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("category", models.CharField(default="Strength", max_length=30)),
                ("duration_minutes", models.PositiveIntegerField(default=30)),
                ("level", models.CharField(default="Beginner", max_length=30)),
                ("description", models.TextField()),
                ("is_featured", models.BooleanField(default=False)),
            ],
        ),
    ]
