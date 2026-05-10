from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight_goal = models.CharField(max_length=255, blank=True)
    allergies = models.TextField(blank=True)
    struggles = models.TextField(blank=True)

    group = models.ForeignKey(
        "Group", on_delete=models.SET_NULL, null=True, related_name="members"
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


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


class Nutrition_plan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    foods = models.ManyToManyField(Food)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.plan_name
