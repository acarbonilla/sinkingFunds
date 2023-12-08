from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path('ws/<str:room_name/', consumers.ChatRoomConsumer.as_asgi()),
]

# re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer),