from django.shortcuts import render, redirect
from .models import Profile, Group, NutritionPlan, Food, DefaultPlan
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def homepage(request):
    return render(request, "homepage.html")


def AboutUs(request):
    return render(request, "about-us.html")


from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profiles/profile-form.html"
    success_url = "/"


class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = UserCreationForm
    success_url = "/auth/login"  # or your home

    # class DeveloperCreateView(CreateView):
    #     model = Developer
    #     form_class = DeveloperForm
    #     template_name = "developers/developer-form.html"
    #     success_url = "/developers/"

    # def form_valid(self, form):
    #     profile = form.save(commit=False)
    #     profile.user = self.request.user
    #     profile.save()

    #     # Generate plan immediately after profile is saved
    #     generate_user_plan(self.request.user, profile)

    #     return super().form_valid(form)


class NutritionPlanListView(ListView):
    model = NutritionPlan
    template_name = "plans/plan-list.html"
    context_object_name = "plans"


def generate_user_plan(user, profile):
    """
    Logic to take the 10 questions and turn them into
    a customized NutritionPlan.
    """

    # 1. Determine which of the 3 Default Plans they need
    if profile.target_weight < profile.current_weight:
        selected_template = DefaultPlan.objects.get(name="weight_loss")
    elif profile.target_weight > profile.current_weight:
        selected_template = DefaultPlan.objects.get(name="muscle_gain")
    else:
        selected_template = DefaultPlan.objects.get(name="maintenance")

    # 2. Basic Calorie Calculation (Example: Simple logic)
    # You can make this more complex using height/weight/age
    calorie_goal = 2000
    if selected_template.name == "weight_loss":
        calorie_goal = 1600
    elif selected_template.name == "muscle_gain":
        calorie_goal = 2800

    # 3. Create the NutritionPlan instance
    new_plan = NutritionPlan.objects.create(
        user=user,
        parent_plan=selected_template,
        daily_calorie_target=calorie_goal,
        special_notes=f"Customized based on {profile.illness_history}",
    )

    # 4. FILTERING LOGIC (Medical/Allergy Customization)
    # Start with all foods in the default template
    safe_foods = selected_template.base_foods.all()

    # If the user listed allergies, exclude those foods
    if profile.allergies:
        # Splits the comma-separated allergies and removes them from the list
        allergy_list = [a.strip() for a in profile.allergies.split(",")]
        for allergy in allergy_list:
            safe_foods = safe_foods.exclude(ingredients__icontains=allergy)
            safe_foods = safe_foods.exclude(name__icontains=allergy)

    # 5. Attach the filtered "Safe Foods" to the User's Plan
    new_plan.customized_foods.set(safe_foods)

    return new_plan
