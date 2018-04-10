# chat/routing.py
from django.conf.urls import url

from . import async_consumers

websocket_urlpatterns = [
    url(r'^', async_consumers.AppConsumer),
]