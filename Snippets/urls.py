from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add/', views.add_snippet_page, name='snippet-add'),
    path('snippets/create/', views.snippet_create, name='snippet-create'),
    path('snippets/edit/<int:snippet_id>/', views.snippet_edit, name='snippet-edit'),
    path('snippets/change', views.snippet_change, name='snippet-change'),
    path('snippets/del/<int:snippet_id>/', views.snippet_del, name='snippet-del'),
    path('snippets/list/', views.snippets_page, name='snippets-list'),
    path('snippets/<int:snippet_id>/', views.snippet_detail, name='snippet-detail')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
