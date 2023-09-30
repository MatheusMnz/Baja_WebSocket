import asyncio
from channels.layers import get_channel_layer
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from .models import SerialDataReader, TelemetryData, HomePage
from asgiref.sync import sync_to_async


class RealTimeDataView(View):
    def get(self, request):
        telemetry_data_dict = {
            'timestamp': '',
            'value1': 0,
            'value2': 0,
            'value3': 0,
            'value4': 0,
            'value5': 0,
            'value6': 0,
            'value7': 0,
        }

        try:
            serial_reader = SerialDataReader(usb_serial_port='/dev/ttyUSB0', baud_rate=115200)
            serial_reader.connect()
            # Leio a porta serial e armazeno os dados em Telemetry
            serial_reader.read_data()

            # Pego sempre o último dado preenchido do DB
            real_data = TelemetryData.objects.last()

            telemetry_data_dict = {
                'timestamp': real_data.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'value1': real_data.value1,
            }

            channel_layer = get_channel_layer()

            # Envio para o grupo dashboard
            sync_to_async(channel_layer.group_send(
                "dashboard",
                {
                    "type": "send.serial.data",
                    "telemetry_data": telemetry_data_dict,
                }
            ))

        except Exception as e:
            # Lide com exceções relacionadas à comunicação serial aqui
            print(f"Erro na leitura de dados em tempo real: {e}")
      

        # Renderize a página com base em um template
        return render(request, 'visualization.html', {'telemetry_data': telemetry_data_dict})


class Home(View):
    def get(self, request):
        home_page = HomePage.objects.first()
        return render(request, 'home.html', {'home_page': home_page})
