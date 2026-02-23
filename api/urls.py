from django.urls import path
from .views import test_api, register_passenger, login_passenger

urlpatterns = [
    path('test/', test_api),
    path('passengers/register/', register_passenger),
    path('passengers/login/', login_passenger),
]
