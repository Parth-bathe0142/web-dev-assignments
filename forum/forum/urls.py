"""
URL configuration for forum project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),

    path("sidebar/", views.sidebar, name="sidebar"),

    path("forums/", views.forum_list, name="forum-list"),
    path(
        "forums/<int:forum_id>/",
        views.forum_detail,
        name="forum-detail",
    ),
    path(
        "forums/create/",
        views.create_forum,
        name="create-forum",
    ),

    path(
        "forums/<int:forum_id>/posts/create-form/",
        views.post_form,
        name="post-form",
    ),
    
    path(
        "forums/<int:forum_id>/posts/create/",
        views.create_post,
        name="create-post",
    ),

    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
]
