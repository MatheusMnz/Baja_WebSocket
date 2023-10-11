from django.db import models
import serial

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

    def __str__(self):
        return f"Data at {self.timestamp}: Value1={self.value1} Value2={self.value1} Value3={self.value1} Value4={self.value1} Value5={self.value1} Value6={self.value1} Value7={self.value1}"


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

                # Separe os pares chave-valor
                pairs = data.split(',')
                values = {}

                for pair in pairs:
                    key, value = pair.strip().split(': ')
                    values[key.strip()] = value.strip()

                pressao_value = values['Pressao']

                if '(' in pressao_value:
                    pressao_value = pressao_value.split('(')[0].strip()

                # Atualize os valores no dicionário serial_data
                self.serial_data['Velocidades Dianteira'] = float(values['Velocidades Dianteira'])
                self.serial_data['Velocidade Traseira'] = float(values['Velocidade Traseira'])
                self.serial_data['RPM'] = float(values['RPM'])
                self.serial_data['Estercamento'] = float(values['Estercamento'])
                self.serial_data['Var_dist'] = float(values['Var_dist'])
                self.serial_data['Consumo'] = float(values['Consumo'])
                self.serial_data['Pressao'] = float(pressao_value)

                # Crie uma instância do modelo TelemetryData e salve os dados
                telemetry_data = TelemetryData(
                    value1=self.serial_data['Velocidades Dianteira'],
                    value2=self.serial_data['Velocidade Traseira'],
                    value3=self.serial_data['RPM'],
                    value4=self.serial_data['Estercamento'],
                    value5=self.serial_data['Var_dist'],
                    value6=self.serial_data['Consumo'],
                    value7=str(self.serial_data['Pressao']),
                )

                # Armazene no Banco de Dados
                telemetry_data.save()
                # print("\nSalvou no Banco de dados!")

                return 1

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

    def __str__(self):
        return self.title


class AboutPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title
