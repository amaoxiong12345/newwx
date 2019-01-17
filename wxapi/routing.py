from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from webs.views import EchoConsumer

application = ProtocolTypeRouter({

    "websocket": AuthMiddlewareStack(
        URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            path("websockettest/", EchoConsumer),
        ]),
    ),
})