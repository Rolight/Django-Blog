from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse


from .models import Article, Comment, Poll, NewUser
from .forms import LoginForm, CommentForm



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

def log_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['uid']
            password = form.cleaned_data['pwd']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                url = request.POST.get('source_url', '/focus')
                return redirect(url)
            else:
                return render(
                    request,
                    'login.html',
                    {
                        'form': form,
                        'error': 'password or username is not true'
                    }
                )
        else:
            return render(
                request,
                'login.html',
                {
                    'form': form
                }
            )

@login_required
def log_out(request):
    url = request.POST.get('source_url', '/focus/')
    logout(request)
    return redirect(url)

def article(request, article_id):
    article=  get_object_or_404(Article, id=article_id)
    content = markdown2.markdown(article.content, extras=[
        "code-friendly", "fenced-code-blocks", "header-ids",
        "toc", "metadata"
    ])
    commentform = CommentForm()
    loginform = LoginForm()
    comments = article.comment_set.all()

    return render(
        request,
        'article_page.html',
        {
            'article': article,
            'loginform': loginform,
            'commentform': commentform,
            'content': 'content',
            'comments': comments
        }
    )

@login_required
def comment(request, article_id):
    form = CommentForm(request.POST)
    url = reverse('focus:article', args=(article_id,))
    if form.is_valid():
        user = request.user
        article = Article.objects.get(id=article_id)
        new_comment = form.cleaned_data['comment']
        c = Comment(content=new_comment, article_id=article_id)
        c.user = user
        c.save()
        article.comment_num += 1
    return redirect(url)

@login_required
def get_keep(request, article_id):
    logged_user = request.user
    article = Article.objects.get(id=article_id)
    articles = logged_user.article_set.all()
    if article not in articles:
        article.user.add(logged_user)
        article.keep_num += 1
        article.save()

        return redirect(reverse('focus:index'))
    else:
        url = reverse('focus:article', args=(article_id))
        return redirect(url)

@login_required
def get_keep(request, article_id):
    logged_user = request.user
    article = Article.objects.get(id=article_id)
    polls = logged_user.poll_set.all()
    articles = []
    for poll in polls:
        articles.append(poll.article)

    if article in articles:
        url = reverse('focus:article', args=(article_id,))
        return redirect(url)
    else:
        article.poll_num += 1
        article.save()
        poll = Poll(user=logged_user, article=article)
        poll.save()
        return redirect(reverse('focus:index'))


