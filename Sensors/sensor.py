from Repository.mongo import Mongo



def dict_snake_to_camel(snake_dict):
    camel_dict = {}
    for key, value in snake_dict.items():
        camel_key = ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(key.split('_')))
        camel_dict[camel_key] = value
    return camel_dict


class Sensor:
    def __init__(self, sensor_name:str, identifier:str, device_id:str, sensor_id:str):
        self.sensor_name = sensor_name
        self.identifier = identifier
        self.device_id = device_id
        self.sensor_id = sensor_id
        self.value = 0
        self.db_collection = Mongo.get_collection("readings")

    def update_value(self, new_value):
        self.value = new_value
        object_to_export = dict_snake_to_camel(self.__dict__)
        object_to_export.pop('dbCollection', None)  # Remove dbCollection if it exists
        self.db_collection.insert_one(object_to_export)


def main():
    sensor = Sensor("Temperature Sensor", "vaginita", "2", "2")
    sensor.update_value(90.0)



if __name__ == "__main__":
    main()
