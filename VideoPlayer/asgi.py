"""
ASGI config for VideoPlayer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from CustomTool import routings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VideoPlayer.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # 自动找urls.py，找视图函数  --> http
    "websocket": URLRouter(routings.websocket_urlpatterns),  # routings(urls)、consumers(views)
})
