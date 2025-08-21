from Sensors.sensor import Sensor

class SensorsGroup:
    def __init__(self, sensors: list[Sensor]):
        self.sensors = sensors

    def add_sensor(self, sensor: Sensor):
        self.sensors.append(sensor)

    def remove_sensor(self, sensor: Sensor):
        self.sensors.remove(sensor)

    def get_sensor_data(self):
        data = {}
        for sensor in self.sensors:
            data[sensor.id] = sensor.get_data()
        return data
    

    def get_sensors_ids(self):
        return [sensor.identifier for sensor in self.sensors]
    

    def update_sensors(self, data: list[dict]):
        for sensor in self.sensors:
            for item in data:
                if sensor.identifier == item["id"]:
                    sensor.update_value(item["value"])

