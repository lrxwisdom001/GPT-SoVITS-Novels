"""
ASGI config for GPT_SoVITS_Novels project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GPT_SoVITS_Novels.settings')

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import voice_synthesis.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GPT_SoVITS_Novels.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            voice_synthesis.routing.websocket_urlpatterns
        )
    ),
})
