import socketio
from Repository.serial import Consultador
from Sensors.sensor import Sensor
from functions.message_parser import parse_serial_message, parse_serial_messages
import threading
import time
from Repository.group_sensors import SensorsGroup

WLB1 = Sensor(sensor_name="Sensor de Proximidad", identifier="WLB1", device_id="1", sensor_id="1")
WLB2 = Sensor(sensor_name="Sensor de Temperatura", identifier="WLB2", device_id="2", sensor_id="2")
WLB3 = Sensor(sensor_name="Sensor de Humedad", identifier="WLB3", device_id="3", sensor_id="3")

sensors_group = SensorsGroup(sensors=[WLB1, WLB2, WLB3])


def sensors_loop():
    while True:
        try:
            datos = Consultador.consultar_datos()
            parsed_messages = parse_serial_messages(datos)

            if parsed_messages:
                print("Datos consultados:", parsed_messages)
                sensors_group.update_sensors(parsed_messages)
        except Exception as e:
            print(f"Error en el bucle de sensores: {e}")
        time.sleep(5)  # Espera 5 segundos antes de la siguiente consulta



def main():
# Cliente síncrono

    # Conectar forzando WebSocket

    sensors_thread = threading.Thread(target=sensors_loop)
    sensors_thread.start()
    sio = socketio.Client(ssl_verify=False)  # quita ssl_verify si tu server tiene SSL válido

    @sio.event
    def connect():
        print("✅ Conectado al servidor")
        # Mandamos el evento para suscribirnos a todos los eventos
        sio.emit("subscribe_all")

    @sio.event
    def subscription_confirmed(data):
        print("📌 Suscripción confirmada:", data)

    @sio.event
    def message(data):
        print("📩 Mensaje recibido:", data)

    @sio.event
    def disconnect():
        print("❌ Desconectado del servidor")

    @sio.event
    def python_trigger(data):
        print("🚀 Evento python_trigger recibido:", data)

    @sio.on('FDR1')
    def alv_handler(data):
        print("👋 Mensaje 'FDR1' recibido:", data)
        if data[0] == 1:
            Consultador.ejecutar_instruccion(instruccion="A", identifier="FDR1")
        elif data[0] == 0:
            Consultador.ejecutar_instruccion(instruccion="S", identifier="FDR1")

    @sio.on('LTR1')
    def hola_handler(data):
        print("👋 Mensaje 'LTR1' recibido:", data)
        if data[0] == 1:
            Consultador.ejecutar_instruccion(instruccion="A", identifier="LTR1")
        elif data[0] == 0:
            Consultador.ejecutar_instruccion(instruccion="S", identifier="LTR1")

    # URL de tu servidor Node/TS con HTTPS
    SERVER_URL = "https://cathubws.kysedomi.lat"  # ejemplo: "https://miapi.midominio.com"

    sio.connect(SERVER_URL, transports=["websocket"])
    sio.wait()

if __name__ == "__main__":
    main()

