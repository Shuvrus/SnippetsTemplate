from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib import auth
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet(request):
    if request.method == 'GET':
        form = SnippetForm()
        context = {
            'form': form,
            'pagename': 'Добавление нового сниппета'
        }
        return render(request, 'pages/add_snippet.html', context)
    elif request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
        return redirect('snippets-list')


def snippets_page(request):
    snippets = Snippet.objects.all()
    sort = request.GET.get('sort')
    lang = request.GET.get("lang")
    if sort:
        snippets = snippets.order_by(sort)
    if lang:
        snippets = snippets.filter(lang=lang)
    quantity_snippets = Snippet.objects.count()
    context = {'pagename': 'Просмотр сниппетов',
               'snippets': snippets,
               'quantity_snippets': quantity_snippets,
               'sort': sort,
               "lang": lang
               }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    comment_form = CommentForm()
    context = {
        'pagename': 'Информация о сниппете',
        'snippet': snippet,
        'comment_form': comment_form,
    }
    return render(request, 'pages/snippet_detail.html', context)


def snippet_del(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    if snippet.user != request.user:
        raise PermissionDenied()
    snippet.delete()
    return redirect('snippets-list')


def snippet_edit(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    context = {
        'snippet': snippet,
    }
    return render(request, 'pages/edit_snippet.html', context)


def snippet_change(request):
    if request.method == 'POST':
        form_data = request.POST
        snippet = Snippet.objects.get(id=form_data['id'])
        snippet.code = form_data['code']
        snippet.save(update_fields=['code'])
    return redirect('snippets-list')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            pass
    return redirect('home')


def logout_page(request):
    auth.logout(request)
    return redirect('home')


def registration(request):
    if request.method == "GET":
        form = UserRegistrationForm()
        context = {
            'pagename': 'Регистрация',
            "form": form
        }
        return render(request, 'pages/registration.html', context)
    elif request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            context = {
                'pagename': 'Регистрация',
                "form": form
            }
            return render(request, 'pages/registration.html', context)
        return redirect('home')

@login_required
def snippets_user(request):
    snippets_user = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': snippets_user
    }
    return render(request, 'pages/view_snippets.html', context)


def comment_create(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        snippet_id = request.POST.get("snippet_id")
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            snippet = Snippet.objects.get(id=snippet_id)
            comment.snippet = snippet
            comment.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
