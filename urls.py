from django.urls import path
from .views import upload_resume
from . import views


urlpatterns = [
    path('', upload_resume, name='upload_resume'),
    path('chatbot/', views.chatbot_interaction, name='chatbot_interaction'),
    path('dashboard/', views.recruitment_dashboard, name='recruitment_dashboard'),
]