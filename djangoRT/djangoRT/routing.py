from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from firstPage.consumer import DashConsumer
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("ws/polData/", DashConsumer.as_asgi()),
    ]),
})
