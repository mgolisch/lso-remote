import click
import requests
import os
from flask import Flask
from flask_sockets import Sockets
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sockets = Sockets(app)
ws_list = []
valid_commands = ["start","split","splitorstart","reset","togglepause",
"undo","skip"] #,"initgametime","setgametime","setloadingtimes","pausegametime","resumegametime"

@sockets.route('/')
def echo_socket(ws):
    ws_list.append(ws)
    while not ws.closed:
        message = ws.receive()
        ws.send(message)

@app.route('/command/<name>')
def recieve_command_via_http(name):
    if not name in valid_commands:
        message = f"Error:command {name} is not a valid command" 
        print(message)
        return message
    print(f"sending message {name}  to all connected clients")
    for ws in ws_list:
        if not ws.closed:
            ws.send(name)
        else:
            # Remove ws if connection closed.
            ws_list.remove(ws)

    return "ok"

@click.group()
def cli():
    pass

@click.command("send-command")
@click.argument("name",type=click.Choice(valid_commands),required=True)
@click.option('--port', default=5000, help='server port')
@click.option('--host', default='localhost', help='server host')
def cli_send_command(name,port,host):
    """connect to lso-remote and send command NAME"""
    if not name in valid_commands:
        click.echo(f"{name} is not a valid command",err=True)
        os.exit(1)
    url = f"http://{host}:{port}/command/{name}"
    click.echo(f"sending command {name}")
    requests.get(url)
    

    
@click.command("run-server")
def cli_start_server():
    """starts the server """
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    click.echo("starting server..")
    click.echo("connect lso to ws://localhost:5000")
    server.serve_forever()

cli.add_command(cli_start_server)
cli.add_command(cli_send_command)

if __name__ == '__main__':
    cli()