import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from .models import SerialDataReader, TelemetryData

class DashConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.groupname='dashboard'

        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
        )

        await self.accept()
        self.serial_reader = SerialDataReader(usb_serial_port='/dev/ttyUSB0', baud_rate=115200)
        self.serial_reader.connect()
        self.send_serial_data()


    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
        self.serial_reader.close()
    
    
    async def send_serial_data(self):
        while True:
            try:
                # Leio os dados da porta serial e armazeno no BD
                await self.serial_reader.read_data() 

                # Pego o último dado inserido no BD
                real_data = TelemetryData.objects.last()

                # Envio o dado para o grupo
                await self.channel_layer.group_send(
                    self.groupname,
                    {
                        'type': 'deprocessing',
                        'value': real_data,
                    }
                )
                await asyncio.sleep(0.5)
            except Exception as e:
                    print(f"Erro ao enviar dados em tempo real via WebSocket: {e}")
                    await asyncio.sleep(5)  # Aguarde antes de tentar novamente


    async def deprocessing(self,event):
        valOther=event['value']
        await self.send(text_data=json.dumps({'value':valOther}))
