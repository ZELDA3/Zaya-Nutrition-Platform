from django.db import models
from django.contrib.auth.models import User


# 1. THE COMMUNITY HUB (For the "Feedback" requirement)
class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    wellness_advice = models.TextField(help_text="General feedback for this group")

    def __str__(self):
        return self.name


# 2. THE USER'S DATA (Full CRUD Target)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Physical Questions
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    current_weight = models.FloatField(null=True, blank=True)
    target_weight = models.FloatField(null=True, blank=True)
    activity_level = models.CharField(
        max_length=50,
        choices=[
            ("sedentary", "Sedentary"),
            ("moderate", "Moderate"),
            ("active", "Active"),
        ],
        null=True,
        blank=True,
    )

    # Medical Questions
    illness_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    dietary_restrictions = models.TextField(blank=True)
    blood_type = models.CharField(max_length=10, blank=True)

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Health Profile"


# 3. THE FOOD LIBRARY
class Food(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    ingredients = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="food_pics/", blank=True)

    def __str__(self):
        return self.name


# 4. THE 3 DEFAULT TEMPLATES (Admin-Managed)
class DefaultPlan(models.Model):
    PLAN_TYPES = [
        ("weight_loss", "Weight Loss"),
        ("muscle_gain", "Muscle Gain"),
        ("maintenance", "Maintenance"),
    ]
    name = models.CharField(max_length=20, choices=PLAN_TYPES, unique=True)
    base_foods = models.ManyToManyField(Food)

    def __str__(self):
        return self.get_name_display()


# 5. THE CUSTOMIZED USER PLAN (The "Logic" Result)
class NutritionPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parent_plan = models.ForeignKey(DefaultPlan, on_delete=models.SET_NULL, null=True)
    customized_foods = models.ManyToManyField(Food)
    daily_calorie_target = models.PositiveIntegerField(null=True, blank=True)
    special_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Active Plan for {self.user.username}"
