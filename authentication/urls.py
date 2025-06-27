from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserMeAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('users/me/', UserMeAPIView.as_view(), name='user-me'),
]
