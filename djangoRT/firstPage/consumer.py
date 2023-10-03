from channels.generic.websocket import AsyncWebsocketConsumer
import json


class DashConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.groupname='dashboard'
        await self.accept()
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
        )
        print('Conectou')



    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
        self.serial_reader.close()
    
    
    async def receive(self, event):
            print("Recebeu um evento no Consumer")
            telemetry_data = event['telemetry_data']
            timestamp = telemetry_data['timestamp']
            value1 = telemetry_data['value1']
            value2 = telemetry_data['value2']
            value3 = telemetry_data['value3']
            value4 = telemetry_data['value4']
            value5 = telemetry_data['value5']
            value6 = telemetry_data['value6']
            value7 = telemetry_data['value7']


            data_to_send = {
                'timestamp': timestamp,
                'value1': value1,
                'value2': value2,
                'value3': value3,
                'value4': value4,
                'value5': value5,
                'value6': value6,
                'value7': value7,
            }

            print(f"Data to send: {data_to_send}")
            await self.send(text_data=json.dumps(data_to_send))
            print("Dados enviados para Canal!")
        