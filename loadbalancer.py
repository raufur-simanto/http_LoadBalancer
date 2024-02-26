import random, requests, yaml, logging

from flask import Flask, request

from utils import load_configuration, transform_backends_from_config, healthcheck, get_healthy_server

loadbalancer = Flask(__name__)

    
config = load_configuration('loadbalancer.yaml')
register = transform_backends_from_config(config)


@loadbalancer.route('/')
def router():
    updated_register = healthcheck(register)
    host_header = request.headers.get('Host')

    for host in config['hosts']:
        if host_header == host['host']:
            healthy_server = get_healthy_server(host['host'], updated_register)
            if not healthy_server:
                return 'No backend servers available.', 503
            response = requests.get(f'http://{healthy_server.endpoint}')
            return response.content, response.status_code

    
@loadbalancer.route('/<path>')
def route_path(path):
    for entry in config['paths']:
        if entry['path'] == f"/{path}":
            response = requests.get(f"http://{random.choice(entry['servers'])}")
            return response.content, response.status_code
    return "not found", 404

    

    