"""
ASGI config for chat_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

'''import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat.middleware import JWTAuthMiddlewareStack
from chat.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_backend.settings')
django.setup()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': JWTAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})
'''

import os
import django

# Indique à Django où se trouvent les settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_backend.settings')

# Initialise Django (obligatoire avant toute importation de modèles ou settings)
django.setup()

# Channels
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.middleware import JWTAuthMiddlewareStack
from chat.routing import websocket_urlpatterns

# HTTP fallback
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
