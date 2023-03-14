import requests
import json
from src.common import config


def get_authentication_token():
    url = 'https://gate.dataloop.ai/token?default'
    data = {
        "username": config.test_email,
        "password": config.test_password,
        "type": "user_credentials"
    }
    reply = requests.post(url=url, data=data)
    return json.loads(reply.content)['id_token']


def get_item_info(item_id, token):
    url = f'https://gate.dataloop.ai/api/v1/items/{item_id}'
    auth_token = token
    hed = {'Authorization': 'Bearer ' + auth_token}
    response = requests.get(url=url, headers=hed)
    return json.loads(response.content)


def get_annotation_info(item_id, token):
    url = f'https://gate.dataloop.ai/api/v1/items/{item_id}/annotations'
    auth_token = token
    hed = {'Authorization': 'Bearer ' + auth_token}
    response = requests.get(url=url, headers=hed)
    return json.loads(response.content)


