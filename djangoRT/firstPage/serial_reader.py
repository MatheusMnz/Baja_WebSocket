import asyncio
from channels.layers import get_channel_layer

from .models import SerialDataReader, TelemetryData
from asgiref.sync import async_to_sync

def read_serial_data():
    try:
        serial_reader = SerialDataReader(usb_serial_port='/dev/ttyUSB0', baud_rate=115200)
        serial_reader.connect()

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

        while True:
            try:
                # Pego dado da serial e armazeno no Banco de Dados
                validation = serial_reader.read_data()

                # Leio o último dado inserido no Banco de Dados
                if validation:
                    real_data = TelemetryData.objects.last()
                    # print(f"Dados obtidos do real_dataBD: {real_data}")
                    telemetry_data_dict = {
                        'timestamp': real_data.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        'value1': real_data.value1,
                        'value2': real_data.value2,
                        'value3': real_data.value3,
                        'value4': real_data.value4,
                        'value5': real_data.value5,
                        'value6': real_data.value6,
                        'value7': real_data.value7, 
                    }
                    
                    # Envio a mensagem primária para o grupo 'dashboard'
                    send_data_to_group(telemetry_data_dict)
                    # print("Enviou dados para o grupo Dashboard!\n")


            except Exception as e:
                print(f"Erro na leitura de dados em tempo real: {e}")
                asyncio.sleep(5)  # Aguarde antes de tentar novamente
    except Exception as e:
        print(f"Erro na conexão com a porta serial: {e}")
        asyncio.sleep(5)  # Aguarde antes de tentar novamente

def send_data_to_group(telemetry_data_dict):
    channel_layer = get_channel_layer()
    group_name = 'dashboard'

    async def send_data():
        await channel_layer.group_add(group_name, 'dash')
        await channel_layer.group_send(
            group_name,
            {
                'type': 'receive',
                'telemetry_data': telemetry_data_dict,
            }
        )

    async_to_sync(send_data)()
