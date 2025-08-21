import serial
import time
import threading


PORT = '/dev/ttyUSB0'

serial_lock = threading.Lock()

class SerialSingleton:
    _instance = None

    @staticmethod
    def get_instance(puerto=PORT, baudrate=9600, timeout=2):
        if SerialSingleton._instance is None:
            SerialSingleton._instance = serial.Serial(puerto, baudrate, timeout=timeout)
            time.sleep(2)
        return SerialSingleton._instance


class Consultador:

    @staticmethod
    def consultar_datos(puerto=PORT, baudrate=9600, timeout=2):
        try:
            with serial_lock:
                ser = SerialSingleton.get_instance(puerto, baudrate, timeout)
                ser.reset_input_buffer()
                ser.write(b"C\n")
                time.sleep(1)

                respuestas = []
                start_time = time.time()
                while True:
                    if ser.in_waiting:
                        respuesta = ser.readline().decode().strip()
                        if respuesta in ["EPI-000", "EPC-000", "EPF-000"]:
                            raise ValueError(f"Error recibido del Arduino: {respuesta}")
                        respuestas.append(respuesta)
                        start_time = time.time()  # Reinicia el tiempo si recibe datos
                    # Sale si no hay datos nuevos por 0.5 segundos o si pasa el timeout
                    if not ser.in_waiting and (time.time() - start_time) > 0.5:
                        break
                    if (time.time() - start_time) > timeout:
                        break
                return respuestas
        except Exception as e:
            print(f"Error al consultar todos los datos: {e}")
            return None




    @staticmethod
    def ejecutar_instruccion(instruccion, identifier, puerto=PORT, baudrate=9600, timeout=2):
        try:
            ser = SerialSingleton.get_instance(puerto, baudrate, timeout)
            comando = f"{instruccion}-{identifier}\n"
            print(comando)
            ser.write(comando.encode())
            time.sleep(1)

            respuesta = ser.readline().decode().strip()
            print(f"Respuesta del Arduino: {respuesta}")
            return respuesta
        except Exception as e:
            print(f"Error al ejecutar instrucción: {e}")
            return None