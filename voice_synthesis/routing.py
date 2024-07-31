from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/status1/', consumers.Status1Consumer.as_asgi()),
    path('ws/status2/', consumers.Status2Consumer.as_asgi()),
]
