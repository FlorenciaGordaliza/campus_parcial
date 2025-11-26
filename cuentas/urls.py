from django.urls import path
from .views import register, UserLoginView, UserLogoutView

app_name = 'cuentas'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]