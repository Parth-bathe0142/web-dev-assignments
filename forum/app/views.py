from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ForumForm, PostForm
from .models import Forum

# Create your views here.


def home(request):
    """
    Full page.
    """
    context = {
        "forum_form": ForumForm(),
        "post_form": PostForm(),
        "login_form": AuthenticationForm(),
        "signup_form": UserCreationForm(),
    }

    return render(request, "forum/home.html", context)


def sidebar(request):
    """
    HTMX fragment containing either the logged-in user
    or the authentication form.
    """
    context = {
        "login_form": AuthenticationForm(),
        "signup_form": UserCreationForm(),
    }

    return render(request, "forum/sidebar.html", context)


def forum_list(request):
    """
    Returns the forum-list.html fragment.
    """
    forums = Forum.objects.all()

    return render(
        request,
        "forum/forum_list.html",
        {"forums": forums},
    )


def forum_detail(request, forum_id):
    """
    Returns the posts belonging to a forum.
    """
    forum = get_object_or_404(Forum, id=forum_id)

    posts = forum.posts.select_related("author").all()

    return render(
        request,
        "forum/post_list.html",
        {
            "forum": forum,
            "posts": posts,
        },
    )


@login_required
def create_forum(request):
    """
    Create a forum through the HTMX modal.
    """
    if request.method != "POST":
        return HttpResponse(status=405)

    form = ForumForm(request.POST)

    if form.is_valid():
        form.save()

        # Return the updated forum list.
        forums = Forum.objects.all()

        return render(
            request,
            "forum/forum_list.html",
            {"forums": forums},
        )

    # Return the form with validation errors.
    return render(
        request,
        "forum/forms/forum_form.html",
        {
            "form": form,
            "modal_name": "forum",
        },
        status=422,
    )


@login_required
def create_post(request, forum_id):
    """
    Create a post in the specified forum.
    """
    if request.method != "POST":
        return HttpResponse(status=405)

    forum = get_object_or_404(Forum, id=forum_id)

    form = PostForm(request.POST)

    if form.is_valid():
        post = form.save(commit=False)
        post.forum = forum
        post.author = request.user
        post.save()

        posts = forum.posts.select_related("author").all()

        return render(
            request,
            "forum/post_list.html",
            {
                "forum": forum,
                "posts": posts,
            },
        )

    return render(
        request,
        "forum/forms/post_form.html",
        {
            "form": form,
            "modal_name": "post",
            "forum": forum,
        },
        status=422,
    )

@login_required
def post_form(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)

    return render(
        request,
        "forum/forms/post_form.html",
        {
            "form": PostForm(),
            "forum": forum,
            "modal_name": "post",
            "open_on_load": True,
        },
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()

    context = {
        "forum_form": ForumForm(),
        "post_form": PostForm(),
        "login_form": form,
        "signup_form": UserCreationForm(),
    }

    return render(
        request,
        "forum/home.html",
        context,
        status=422 if request.method == "POST" else 200,
    )


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    context = {
        "forum_form": ForumForm(),
        "post_form": PostForm(),
        "login_form": AuthenticationForm(),
        "signup_form": form,
    }

    return render(
        request,
        "forum/home.html",
        context,
        status=422 if request.method == "POST" else 200,
    )


def logout_view(request):
    if request.method == "POST":
        logout(request)

    return redirect("home")