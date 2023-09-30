from django.db import models
import serial
import json

#---------------------------------------------------------------------------------------------------
class TelemetryData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    value1 = models.FloatField(null=True)
    value2 = models.FloatField(null=True)
    value3 = models.FloatField(null=True)
    value4 = models.FloatField(null=True)
    value5 = models.FloatField(null=True)
    value6 = models.FloatField(null=True)
    value7 = models.TextField(null=True)

    def _str_(self):
        return f"Data at {self.timestamp}: Value1={self.value1}, Value2={self.value2}, Value3={self.value3}, Value4={self.value4}, Value5={self.value5}, Value6={self.value6}, Value7={self.value7}"


class SerialDataReader:
    def __init__(self, usb_serial_port='/dev/ttyUSB0', baud_rate=115200):
        self.usb_serial_port = usb_serial_port
        self.baud_rate = baud_rate
        self.ser = None
        self.serial_data = {
            'velocidade_dianteira': 0.0,
            'velocidade_traseira': 0.0,
            'rpm': 0.0,
            'esterçamento': 0.0,
            'var_dist': 0.0,
            'consumo': 0.0,
            'pressao': (0.0, 0.0),
        }

        
    def connect(self):
        try:
            self.ser = serial.Serial(self.usb_serial_port, self.baud_rate, timeout=1)
        except serial.serialutil.SerialException as e:
            print(f"Serial port error: {e}")
            self.ser = None

    def read_data(self):
        if self.ser is not None:
            try:
                data = self.ser.readline().decode('utf-8').strip()
                values = data.split(',')
                # if len(values) == 7:
                #     (
                #         vel_dianteira,
                #         vel_traseira,
                #         rpm,
                #         esterçamento,
                #         var_dist,
                #         consumo,
                #         pressao,
                #     ) = map(lambda s: str(s.split(': ')[1]), values)

                #     # Atualize as variáveis com os valores lidos
                #     self.serial_data['velocidade_dianteira'] = vel_dianteira
                #     self.serial_data['velocidade_traseira'] = vel_traseira
                #     self.serial_data['rpm'] = rpm
                #     self.serial_data['esterçamento'] = esterçamento
                #     self.serial_data['var_dist'] = var_dist
                #     self.serial_data['consumo'] = consumo
                #     self.serial_data['pressao'] = pressao

                #     # Crie uma instância do modelo TelemetryData e salve os dados
                #     telemetry_data = TelemetryData(
                #         value1=float(vel_dianteira), 
                #         value2=float(vel_traseira),
                #         value3=float(rpm),
                #         value4=float(esterçamento),
                #         value5=float(var_dist),
                #         value6=float(consumo),
                #         value7=str(pressao),
                #     )
                #     telemetry_data.save()
                #     print(self.serial_data)


                # Teste
                print(values)
                if len(values) == 1:
                    vel_dianteira = values[0].split(':')[1]
                    self.serial_data['velocidade_dianteira'] = vel_dianteira
                    telemetry_data = TelemetryData(
                        value1=float(vel_dianteira)
                    )
                    telemetry_data.save()

            except KeyboardInterrupt:
                print("Keyboard interrupt. Exiting...")
            except serial.serialutil.SerialException as e:
                print(f"Serial communication error: {e}")

    def get_serial_data(self):
        return self.serial_data

    def close(self):
        if self.ser:
            self.ser.close()
#---------------------------------------------------------------------------------------------------



class HomePage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def _str_(self):
        return self.title


class AboutPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def _str_(self):
        return self.title
