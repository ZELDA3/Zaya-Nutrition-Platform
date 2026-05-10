from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage),
    path("about/", views.AboutUs),
    path("sign-up/", views.SignUpView.as_view()),
    path("profile/", views.ProfileCreateView.as_view(), name="profile"),
    path("plans/", views.NutritionPlanListView.as_view()),
]
