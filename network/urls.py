
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-post", views.new_post, name="new_post"),
    path("<str:username>/", views.profile_page, name="profile_page"),
    path("following", views.following_page, name="following_page"),
]