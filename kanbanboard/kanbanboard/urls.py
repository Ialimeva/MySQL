from django.contrib import admin
from django.urls import path, include
from home.views import home_view, addtask, updatetask, deletetask
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', home_view, name = 'home'),
    path('add_task/', addtask, name = 'addtask'),
    path('update_task/<str:pk>/', updatetask, name = 'updatetask'),
    path('delete_task/<str:pk>/', deletetask, name = 'deletetask'),
]
