from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Group, NutritionPlan, Food, DefaultPlan
from .forms import ProfileForm, NutritionPlanForm


# -- Basic Views --
def homepage(request):
    return render(request, "homepage.html")


def AboutUs(request):
    return render(request, "about-us.html")


# -- Authentication --
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = "/auth/login/"


# -- Profile CRUD (The Core Requirement) --
class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profiles/profile-form.html"
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        profile = form.save()
        generate_user_plan(self.request.user, profile)
        return super().form_valid(form)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profiles/profile-detail.html"
    context_object_name = "profile"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profiles/profile-form.html"
    success_url = "/plans/"

    def form_valid(self, form):
        profile = form.save()
        # Regenerate plan if they changed their weight/allergies
        generate_user_plan(self.request.user, profile)
        return super().form_valid(form)


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    success_url = "/"

    # This allows the delete to happen without a separate confirmation page
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


# -- Plan Reading --
class NutritionPlanListView(LoginRequiredMixin, ListView):
    model = NutritionPlan
    template_name = "plans/plan-list.html"
    context_object_name = "plans"


class NutritionPlanDetailView(LoginRequiredMixin, DetailView):
    model = NutritionPlan
    template_name = "plans/plan-details.html"
    context_object_name = "plan"


class NutritionPlanUpdateView(LoginRequiredMixin, UpdateView):
    model = NutritionPlan
    form_class = NutritionPlanForm
    template_name = "plans/plan-form.html"
    success_url = "/plans/"


class NutritionPlanDeleteView(LoginRequiredMixin, DeleteView):
    model = NutritionPlan
    success_url = "/"

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


## the group views


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "groups/wellness-group.html"
    context_object_name = "groups"


# -- THE LOGIC ENGINE --
def generate_user_plan(user, profile):
    # 1. Select Template
    if profile.target_weight < profile.current_weight:
        selected_template = DefaultPlan.objects.get(name="weight_loss")
    elif profile.target_weight > profile.current_weight:
        selected_template = DefaultPlan.objects.get(name="muscle_gain")
    else:
        selected_template = DefaultPlan.objects.get(name="maintenance")

    # 2. Set Calories
    calorie_map = {"weight_loss": 1600, "muscle_gain": 2800, "maintenance": 2000}
    goal_calories = calorie_map.get(selected_template.name, 2000)

    # 3. Create or Update Plan
    plan, created = NutritionPlan.objects.get_or_create(user=user)
    plan.parent_plan = selected_template
    plan.daily_calorie_target = goal_calories
    plan.save()

    # 4. Filter Foods by Allergies
    safe_foods = selected_template.base_foods.all()
    if profile.allergies:
        allergy_list = [a.strip().lower() for a in profile.allergies.split(",")]
        for allergy in allergy_list:
            safe_foods = safe_foods.exclude(ingredients__icontains=allergy)

    plan.customized_foods.set(safe_foods)
    return plan
