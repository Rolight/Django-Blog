from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist

from .models import Article, Comment, Poll, NewUser
from .forms import LoginForm


# Create your views here.
import markdown2

def index(request):
    latest_article_list = Article.objects.query_by_time()
    loginform = LoginForm()

    context = {
        'latest_article_list': latest_article_list,
        'loginform': loginform
    }

    return render(request, 'index.html', context)


