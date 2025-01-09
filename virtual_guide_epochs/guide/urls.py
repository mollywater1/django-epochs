from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('era/<int:pk>/', views.era_detail, name='era_detail'),
    path('era/<int:pk>/quiz/', views.quiz, name='quiz'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='guide/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('era/<int:pk>/mini-game/', views.mini_game, name='mini_game'),
    path('lecture/<int:pk>/', views.lecture_detail, name='lecture_detail'),

]
