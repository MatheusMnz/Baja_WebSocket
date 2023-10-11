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
        return render(request, 'home_final.html')
    
class Subsystems(View):
    def get(self, request):
        return render(request, 'subsistemas.html')

class Eletronica(View):
    def get(self, request):
        return render(request, 'eletronica.html')  # Nome do template correspondente
    
class Calculo(View):
    def get(self, request):
        return render(request, 'subsistemas.html')  # Nome do template correspondente
    
class Freio(View):
    def get(self, request):
        return render(request, 'subsistemas.html')  # Nome do template correspondente
    
class Marketing(View):
    def get(self, request):
        return render(request, 'subsistemas.html')  # Nome do template correspondente
    
class Suspensao(View):
    def get(self, request):
        return render(request, 'subsistemas.html')  # Nome do template correspondente
