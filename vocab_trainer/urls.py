from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('trainer.urls')),
    # Custom auth URLs
    path('login/',
         auth_views.LoginView.as_view(
             template_name='registration/login.html',
            #  redirect_authenticated_user=True,
             next_page='/'
         ), 
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]