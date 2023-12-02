from http.server import BaseHTTPRequestHandler
from urllib import parse
import http.server
import ssl
import io

class SecureHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        ruta_analizada = parse.urlparse(self.path)
        partes_del_mensaje = [
            'Valores del cliente:',
            'Dirección={} ({})'.format(
                self.client_address,
                self.address_string()),
            'Comando={}'.format(self.command),
            'Ruta={}'.format(self.path),
            'Ruta real={}'.format(ruta_analizada.path),
            'Consulta={}'.format(ruta_analizada.query),
            'Versión de petición={}'.format(self.request_version),
            '',
            'Valores del servidor:',
            'Versión del servidor={}'.format(self.server_version),
            'Versión del sistema={}'.format(self.sys_version),
            'Versión del protocolo={}'.format(self.protocol_version),
            '',
            'Encabezados Recibidos:',
        ]
        for name, value in sorted(self.headers.items()):
            partes_del_mensaje.append(
                '{}={}'.format(name, value.rstrip())
            )
        partes_del_mensaje.append('')
        mensaje = '\r\n'.join(partes_del_mensaje)
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(mensaje.encode('utf-8'))

    def do_POST(self):
        # Analizar los datos publicados en el formulario
        formulario = parse.parse_qs(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
        
        # Comenzar la respuesta
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()

        out = io.TextIOWrapper(
            self.wfile,
            encoding='utf-8',
            line_buffering=False,
            write_through=True,
        )

        out.write('Cliente: {}\n'.format(self.client_address))
        out.write('Agente - Usuario: {}\n'.format(
            self.headers['user-agent']))
        out.write('Ruta: {}\n'.format(self.path))
        out.write('Datos del formulario:\n')

        # Devolver información sobre lo que se publicó en el formulario
        for campo, valor in formulario.items():
            out.write('\t{}={}\n'.format(
                campo, ', '.join(valor)))

        # Desconectar el wrapper
        out.detach()

if __name__ == '__main__':
    host = 'localhost'
    port = 8444

    # Configurar el contexto SSL
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')  

    # Crear un socket seguro
    with http.server.ThreadingHTTPServer((host, port), SecureHandler) as server:
        server.socket = context.wrap_socket(server.socket, server_side=True)
        print(f'Servidor seguro iniciado en https://{host}:{port}')

        # Iniciar el servidor HTTP con el manejador seguro
        server.serve_forever()
