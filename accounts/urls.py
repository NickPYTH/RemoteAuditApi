from django.urls import path
from .views import CreateProfile, GetProfile, UpdateProfile, DeleteProfile

urlpatterns = [
    path("create-profile", CreateProfile.as_view(), name="create-profile"),
    path("get-profile", GetProfile.as_view(), name="get-profile"),
    path("update-profile", UpdateProfile.as_view(), name="update-profile"),
    path("delete-profile", DeleteProfile.as_view(), name="delete-profile"),
]
