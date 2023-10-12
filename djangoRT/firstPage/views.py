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
        return render(request, 'home.html')
    
class Subsystems(View):
    def get(self, request):
        return render(request, 'subsistemas.html')

class Eletronica(View):
    def get(self, request):
        return render(request, 'eletronica.html')
    
class Calculo(View):
    def get(self, request):
        return render(request, 'calculo.html')
    
class Powertrain(View):
    def get(self, request):
        return render(request, 'powertrain.html')
    
class Freio(View):
    def get(self, request):
        return render(request, 'freio.html')
    
class Marketing(View):
    def get(self, request):
        return render(request, 'marketing.html')
    
class Suspensao(View):
    def get(self, request):
        return render(request, 'suspensao.html')
    
class About(View):
    def get(self, request):
        return render(request, 'about.html')

class Contact(View):
    def get(self, request):
        return render(request, 'contact.html')

class Partners(View):
    def get(self, request):
        return render(request, 'partners.html')
