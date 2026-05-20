from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_endpoint, name='test'),
    path('analyze/', views.analyze_endpoint, name='analyze'),
    path('chat/', views.chat_endpoint, name='chat'),
]
