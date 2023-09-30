from django.conf import settings
from django.contrib import admin
from django.urls import path
from firstPage import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home.as_view(),name='home'),
    path('visualization/', views.RealTimeDataView.as_view(), name='real_time_visualization')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

