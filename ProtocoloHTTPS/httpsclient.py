import http.client
import os
import urllib.parse

def get(host, port, path, cert_file, key_file):
    # Crear conexión segura al servidor con certificado y clave privada de prueba
    connection = http.client.HTTPSConnection(
        host, port, key_file=key_file, cert_file=cert_file, context=http.client.ssl._create_unverified_context()
    )

    # Realizar solicitud GET al servidor
    connection.request("GET", path)

    # Obtener la respuesta del servidor
    response = connection.getresponse()

    # Imprimir la respuesta del servidor
    print(f"Status: {response.status}")
    print(response.read().decode('utf-8'))

    # Cerrar la conexión
    connection.close()

def post(host, port, path, cert_file, key_file, form_data):
    # Crear conexión segura al servidor con certificado y clave privada de prueba
    connection = http.client.HTTPSConnection(
        host, port, key_file=key_file, cert_file=cert_file, context=http.client.ssl._create_unverified_context()
    )

    # Convertir datos del formulario a formato URL-encoded
    body = urllib.parse.urlencode(form_data)

    # Cabeceras de la solicitud POST
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': len(body),
    }

    # Realizar solicitud POST al servidor
    connection.request("POST", path, body, headers)

    # Obtener la respuesta del servidor
    response = connection.getresponse()

    # Imprimir la respuesta del servidor
    print(f"Status: {response.status}")
    print(response.read().decode('utf-8'))

    # Cerrar la conexión
    connection.close()

if __name__ == '__main__':
    server_host = 'localhost'
    server_port = 8444
    server_path = '/'
    script_directory = os.path.dirname(os.path.realpath(__file__))
    cert_file = os.path.join(script_directory, 'server.crt')
    key_file = os.path.join(script_directory, 'server.key')

    # Realizar solicitud GET
    get(server_host, server_port, server_path, cert_file, key_file)

    # Obtener datos del formulario desde el usuario
    form_data = {}
    while True:
        key = input("Ingrese el nombre del campo (o 'fin' para terminar): ")
        if key.lower() == 'fin':
            break
        value = input(f"Ingrese el valor para {key}: ")
        form_data[key] = value

    # Realizar solicitud POST con datos dinámicos del formulario
    post(server_host, server_port, server_path, cert_file, key_file, form_data)