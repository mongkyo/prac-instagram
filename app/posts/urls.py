from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post-list' ),
    path('create/', views.post_create, name='post-create')
]