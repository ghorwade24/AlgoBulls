from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.register,name='register_page'),
    path('login/',views.login,name='login_page'),
    path('logout/',views.logout_view,name='logout'),
    path('home_page/',views.todo,name='Home_page'),
    path('api/create/', views.create_task, name='api_create_task'),
    path('api/update/<int:task_id>/', views.update_task, name='api_update_task'),
    path('api/delete/<int:task_id>/', views.delete_task, name='api_delete_task'),

]