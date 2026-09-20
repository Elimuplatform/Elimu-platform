from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('ai-tutor/', views.ai_tutor, name='ai_tutor'),
    path('game/', views.jet_game, name='jet_game'),
]