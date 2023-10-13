from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from application import views
# from .views import AccountCreate

urlpatterns = [
    path('auth/', include('social_django.urls', namespace='social')),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path("", views.home, name='home'),
    # path('accountcreate/', AccountCreate.as_view(), name = 'accountcreate'),
    path('accountcreate/', views.account_create, name = 'accountcreate'),
    path('company/', views.company, name = 'company'),
]