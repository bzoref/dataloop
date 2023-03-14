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


def calculate_annotation_starting_and_ending_point(image_container_data):
    image_start_x_point = round(image_container_data['x'])
    image_start_y_point = round(image_container_data['y'])
    image_width = round(image_container_data['width'])
    image_width_quarter = image_width/4
    image_height = round(image_container_data['height'])
    image_height_quarter = image_height/4
    annotation_x_start_point = round(image_start_x_point + image_width_quarter)
    annotation_y_start_point = round(image_start_y_point + image_height_quarter)
    annotation_x_end_point = round(image_start_x_point + 3*image_width_quarter)
    annotation_y_end_point = round(image_start_y_point + 3*image_height_quarter)
    return dict(
        annotation_x_start_point=annotation_x_start_point,
        annotation_y_start_point=annotation_y_start_point,
        annotation_x_end_point=annotation_x_end_point,
        annotation_y_end_point=annotation_y_end_point
    )





