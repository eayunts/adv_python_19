from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "blog"

urlpatterns = [
    path('home', views.BlogList, name='home'),  
    path('blogposts/<slug:slug>/', views.PostList, name='post_list'),
    path('post-create/', views.post_create, name='post_create'),
    path('post/<slug:slug>/', views.PostDetail, name='post_detail'),
    path('post-update/<int:id>/', views.post_update, name='post_update'),
    path('post/<slug:postid>/preference/<userpreference>/', views.postpreference, name='postpreference'),
] 

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)