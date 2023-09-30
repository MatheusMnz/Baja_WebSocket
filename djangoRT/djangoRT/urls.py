from django.contrib import admin
from django.urls import path
from firstPage import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='Home'),
]


from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from firstPage.consumer import DashConsumer  # Substitua pelo caminho correto do seu consumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/polData/", DashConsumer.as_asgi()),  # Substitua pelo caminho correto do seu consumer
    ]),
})