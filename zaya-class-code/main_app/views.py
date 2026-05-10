from django.shortcuts import render
from .models import Profile, Group, Nutrition_plan, Food

# Create your views here.


def homepage(request):
    return render(request, "homepage.html")


from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)


class Nutrition_planListView(ListView):
    model = Nutrition_plan
