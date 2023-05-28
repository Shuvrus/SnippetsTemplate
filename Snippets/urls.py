from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add/', views.add_snippet, name='snippet-add'),
    path('snippets/edit/<int:snippet_id>/', views.snippet_edit, name='snippet-edit'),
    path('snippets/change', views.snippet_change, name='snippet-change'),
    path('snippets/<int:snippet_id>/del', views.snippet_del, name='snippet-del'),
    path('snippets/list/', views.snippets_page, name='snippets-list'),
    path('snippets/<int:snippet_id>/', views.snippet_detail, name='snippet-detail'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.registration, name='registration'),
    path('snippets/user/', views.snippets_user, name='snippets-user'),
    path('comment/create', views.comment_create, name="comment-create"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
