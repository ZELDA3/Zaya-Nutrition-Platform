from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "current_weight",
            "target_weight",
            "height",
            "age",
            "illness_history",
            "allergies",
        ]


# class Form_valid(forms.ModelForm):
#     class Meta:
#         model = Profile
