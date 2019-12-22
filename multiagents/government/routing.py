from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^agent/ws/(?P<room_name>[^/]+)/$', consumers.AgentConsumer),
]
