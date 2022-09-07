from django.urls import re_path

from CustomTool import consumers

websocket_urlpatterns = [
    re_path(r'live/ws/(?P<room_id>\w+)/$', consumers.ChatConsumer.as_asgi())
]