"""
ejemplo de mensaje serial -> WLB1:500 (donde WLB es el id del sensor y 500 el valor de la lectura)



"""

def parse_serial_message(message: str) -> dict:
    """
    Parsea un mensaje serial en el formato 'ID:valor' y devuelve un diccionario con el ID y el valor.

    Args:
        message (str): El mensaje serial a parsear.

    Returns:
        dict: Un diccionario con el ID y el valor.
    """
    try:
        id_, value = message.split(':')
        return {'id': id_.strip(), 'value': float(value.strip())}
    except ValueError as e:
        print(f"Error al parsear el mensaje '{message}': {e}")
        return None
    

def parse_serial_messages(messages: list[str]) -> list[dict]:
    """
    Parsea una lista de mensajes seriales en el formato 'ID:valor' y devuelve una lista de diccionarios con los ID y los valores.

    Args:
        messages (list[str]): La lista de mensajes seriales a parsear.

    Returns:
        list[dict]: Una lista de diccionarios con los ID y los valores.
    """
    return [parse_serial_message(msg) for msg in messages]


def main():
    message = "WLB1:500"
    parsed_message = parse_serial_message(message)
    if parsed_message:
        print(f"Mensaje parseado correctamente: {parsed_message}")
        print(f"ID: {parsed_message['id']}, Valor: {parsed_message['value']}")

    messages = ["WLB1:500", "WLB2:600", "WLB3:700"]
    parsed_messages = parse_serial_messages(messages)
    print(parsed_messages)
    for pm in parsed_messages:
        if pm:
            print(f"Mensaje parseado correctamente: {pm}")
            print(f"ID: {pm['id']}, Valor: {pm['value']}")

if __name__ == "__main__":
    main()