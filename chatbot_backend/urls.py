
from django.contrib import admin
from django.urls import path,include
from chatbot_api.views import chat

urlpatterns = [
    path('', include('chatbot_api.urls')),
    # path('admin/', admin.site.urls),
]
