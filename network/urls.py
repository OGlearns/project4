
from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-post", views.new_post, name="new_post"),
    path("<str:username>/", views.profile_page, name="profile_page"),
    path("following", views.following_page, name="following_page"),

    # API ROUTES
    path("update_likes", views.update_likes, name="update_likes"),
    path("follow", views.follow, name="follow"),
    path("edit_post", views.edit_post, name="edit_post"),

    #FavIcon Route
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),
]
