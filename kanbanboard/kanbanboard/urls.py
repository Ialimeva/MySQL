from django.contrib import admin
from django.urls import path, include
from home.views import home_view, addtask, updatetask, deletetask, register_user, statistics_view, logout_view
from django.contrib.auth.views import LoginView
from home import views

urlpatterns = [
    path('', LoginView.as_view(template_name = 'login.html'), name = 'login'),
    path('register/', register_user, name = 'register'),
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/profile/', home_view, name = 'home'),
    path('add_task/', addtask, name = 'addtask'),
    path('update_task/<str:pk>/', updatetask, name = 'updatetask'),
    path('delete_task/<str:pk>/', deletetask, name = 'deletetask'),
    path('statistics/', statistics_view, name='statistics'),
    path('update-task-status/', views.update_task_status, name='update_task_status'),
    path('logout/', logout_view, name='logout'),
]
