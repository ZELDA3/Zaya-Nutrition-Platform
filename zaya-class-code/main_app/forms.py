from django import forms
from .models import Profile, NutritionPlan


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "age",
            "height",
            "current_weight",
            "target_weight",
            "activity_level",
            "illness_history",
            "allergies",
            "medications",
            "dietary_restrictions",
            "blood_type",
        ]
        widgets = {
            "illness_history": forms.Textarea(
                attrs={"rows": 2, "placeholder": "e.g. Diabetes, Hypertension"}
            ),
            "allergies": forms.Textarea(
                attrs={"rows": 2, "placeholder": "e.g. Peanuts, Shellfish"}
            ),
        }


class NutritionPlanForm(forms.ModelForm):
    class Meta:
        model = NutritionPlan
        fields = [
            "user",
            "parent_plan",
            "customized_foods",
            "daily_calorie_target",
            "special_notes",
        ]
