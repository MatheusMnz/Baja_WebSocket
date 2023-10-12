from django.conf import settings
from django.contrib import admin
from django.urls import path
from firstPage import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home.as_view(),name='home'),
    path('subsistemas/', views.Subsystems.as_view(), name='subsistemas'),
    path('subsistemas/eletronica', views.Eletronica.as_view(), name='eletronica'),
    path('subsistemas/calculo', views.Calculo.as_view(), name='calculo'),
    path('subsistemas/freio', views.Freio.as_view(), name='freio'),
    path('subsistemas/marketing', views.Marketing.as_view(), name='marketing'),
    path('subsistemas/powetrain', views.Powertrain.as_view(), name='powertrain'),
    path('subsistemas/suspensao', views.Suspensao.as_view(), name='suspensao'),
    path('sobre', views.About.as_view(), name='about'),
    path('contato', views.Contact.as_view(), name='contact'),
    path('parceiros', views.Partners.as_view(), name='partners'),
    path('subsistemas/eletronica/telemetria', views.RealTimeDataView.as_view(), name='telemetria'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

