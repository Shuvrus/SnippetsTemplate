from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    form = SnippetForm()
    context = {
        'form': form,
        'pagename': 'Добавление нового сниппета'
    }
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    quantity_snippets = len(snippets)
    context = {'pagename': 'Просмотр сниппетов',
               'snippets': snippets,
               'quantity_snippets': quantity_snippets
               }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    context = {
        'pagename': 'Информация о сниппете',
        'snippet': snippet
    }
    return render(request, 'pages/snippet_detail.html', context)


def snippet_create(request):
    if request.method == "POST":
        # form_data = request.POST
        # snippet = Snippet(
        #     name=form_data['name'],
        #     lang=form_data['lang'],
        #     code=form_data['code'],
        # )
        # snippet.save()
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('snippets-list')


def snippet_del(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
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
