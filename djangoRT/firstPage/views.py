from django.views import View
from django.shortcuts import render
from .serial_reader import read_serial_data
from .models import HomePage
import threading


class RealTimeDataView(View):
    def get(self, request):
    # Iniciar a thread para processar read_serial_data
        thread = threading.Thread(target=read_serial_data)
        thread.start()
        return render(request, 'visualization.html')


class Home(View):
    def get(self, request):
        home_page = HomePage.objects.first()
        return render(request, 'home.html', {'home_page': home_page})
