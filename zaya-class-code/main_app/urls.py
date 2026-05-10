from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage),
    path("about/", views.AboutUs),
    path("plans/", views.Nutrition_planListView.as_view()),
]
