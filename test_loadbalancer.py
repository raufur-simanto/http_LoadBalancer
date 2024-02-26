import pytest

from loadbalancer import loadbalancer

@pytest.fixture
def client():
    with loadbalancer.test_client() as client:
        yield client


# def test_hello(client):
#     result = client.get('/')
#     assert b'hello' in result.data

## host based routing
def test_host_routing_mango(client):
    result = client.get('/', headers={'Host': 'www.mango.com'})
    assert b'This is the mango application' in result.data

def test_host_routing_apple(client):
    result = client.get('/', headers={'Host': 'www.apple.com'})
    assert b'This is the apple application' in result.data

def test_host_routing_notfound(client):
    result = client.get('/', headers={'Host': 'www.notmango.com'})
    assert b'not found' in result.data
    assert 404==result.status_code


### path based routing test
def test_path_routing_mango(client):
    result = client.get('/mango')
    assert b'This is the mango application' in result.data

def test_path_routing_apple(client):
    result = client.get('/apple')
    assert b'This is the apple application' in result.data

def test_path_routing_notfound(client):
    result = client.get('/notmango')
    assert b'not found' in result.data
    assert 404 == result.status_code