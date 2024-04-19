from django.urls import path
from . import views

app_name = 'chatapp'

urlpatterns = [
    path('chatbot/', views.chatbot_html, name='chatbot_api'),
    path('chat', views.chat, name='chat'),
    path('', views.login_view, name='login_page'),
]