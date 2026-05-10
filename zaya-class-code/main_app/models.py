from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # --- Physical Questions (Examples) ---
    age = models.PositiveIntegerField(null=True)
    height = models.FloatField(null=True)
    current_weight = models.FloatField(null=True)
    target_weight = models.FloatField(null=True)
    activity_level = models.CharField(
        max_length=50,
        choices=[
            ("sedentary", "Sedentary"),
            ("moderate", "Moderate"),
            ("active", "Active"),
        ],
    )

    # --- Medical Questions (Examples) ---
    illness_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    dietary_restrictions = models.TextField(blank=True)
    blood_type = models.CharField(max_length=10, blank=True)

    # Link to the Group for community feedback
    group = models.ForeignKey("Group", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username}'s Health Data"


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    wellness_advice = models.TextField(help_text="Genaral feedback for this group")

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    image = models.ImageField(upload_to="food_pics/", blank=True)


class NutritionPlan(models.Model):
    # This links the specific customized instance to the user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    PLAN_TYPES = [
        ("weight_loss", "Weight Loss"),
        ("muscle_gain", "Muscle Gain"),
        ("maintenance", "Maintenance"),
    ]
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)

    # This stores the specific food items that are safe for THIS user
    customized_foods = models.ManyToManyField("Food")

    daily_calorie_target = models.PositiveIntegerField()
    special_notes = models.TextField(blank=True)  # e.g., "Avoid Gluten"

    def __str__(self):
        return f"{self.plan_type} for {self.user.username}"
