from django.contrib import admin
from django.urls import path, include, re_path
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
    path('company/<int:num>/', views.company, name = 'company_pagination'),
    path("information/", views.information, name='information'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('application_create/<path:company_name>/', views.application_create, name='application_create'),

    path('application_detail/<int:pk>/', views.application_detail, name='application_detail'),
    path('application/<int:pk>/edit/', views.edit_application, name='edit_application'),
    path('generate_pdf/<int:pk>/', views.generate_pdf, name='generate_pdf'),
    path('application_list/', views.application_list, name='application_list'),

]