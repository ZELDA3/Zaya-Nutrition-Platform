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
]
