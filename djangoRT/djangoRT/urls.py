from django.conf import settings
from django.contrib import admin
from django.urls import path
from firstPage import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',views.Home.as_view(),name='home'),
    path('',views.Home.as_view(),name='home-final'),
    path('subsistemas/', views.Subsystems.as_view(), name='subsistemas'),
    path('subsistemas/eletronica', views.Eletronica.as_view(), name='eletronica'),
    path('subsistemas/calculo', views.Eletronica.as_view(), name='calculo'),
    path('subsistemas/freio', views.Eletronica.as_view(), name='freio'),
    path('subsistemas/marketing', views.Eletronica.as_view(), name='marketing'),
    path('subsistemas/powetrain', views.Eletronica.as_view(), name='powertrain'),
    path('subsistemas/suspensao', views.Eletronica.as_view(), name='suspensao'),
    path('subsistemas/eletronica/telemetria', views.RealTimeDataView.as_view(), name='telemetria'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

