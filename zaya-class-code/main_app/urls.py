from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage),
    path("about/", views.AboutUs),
    path("sign-up/", views.SignUpView.as_view()),
    # Profile CRUD
    path("profile/create/", views.ProfileCreateView.as_view(), name="profile_create"),
    path("profile/<int:pk>/", views.ProfileDetailView.as_view(), name="profile_detail"),
    path(
        "profile/<int:pk>/update/",
        views.ProfileUpdateView.as_view(),
        name="profile_update",
    ),
    path(
        "profile/<int:pk>/delete/",
        views.ProfileDeleteView.as_view(),
        name="profile_delete",
    ),
    # Plans
    path("plans/", views.NutritionPlanListView.as_view(), name="plan_list"),
    path(
        "plans/<int:pk>/",
        views.NutritionPlanDetailView.as_view(),
        name="profile_detail",
    ),
    path("plans/<int:pk>/update/", views.NutritionPlanUpdateView.as_view()),
    path(
        "plans/<int:pk>/delete/",
        views.NutritionPlanDeleteView.as_view(),
        name="plan_delete",
    ),
    path("groups/", views.GroupListView.as_view()),
]
