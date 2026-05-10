from django.db import models
from django.contrib.auth.models import User


# 1. THE COMMUNITY HUB
class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    wellness_advice = models.TextField(help_text="General feedback for this group")

    def __str__(self):
        return self.name


# 2. THE USER'S DATA (10 Questions)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Physical Questions
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

    # Medical Questions
    illness_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    dietary_restrictions = models.TextField(blank=True)
    blood_type = models.CharField(max_length=10, blank=True)

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username}'s Health Profile"


# 3. THE FOOD LIBRARY
class Food(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    # Adding null=True and blank=True lets the database accept empty values
    ingredients = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="food_pics/", blank=True)

    def __str__(self):
        return self.name


# 4. THE 3 DEFAULT TEMPLATES (Managed in Admin)
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


# 5. THE CUSTOMIZED USER PLAN
class NutritionPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parent_plan = models.ForeignKey(DefaultPlan, on_delete=models.SET_NULL, null=True)

    # This stores ONLY the foods safe for this specific user
    customized_foods = models.ManyToManyField(Food)

    daily_calorie_target = models.PositiveIntegerField()
    special_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Active {self.parent_plan} for {self.user.username}"
