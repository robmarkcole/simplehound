"""
Simplehound core.
"""
import base64
from typing import Dict, List, Set, Union
import json

import requests
from PIL import Image

## Const
HTTP_OK = 200
DEFAULT_TIMEOUT = 10  # seconds

## API urls
URL_DETECTIONS = "https://dev.sighthoundapi.com/v1/detections"

DETECTIONS_PARAMS = (
    ("type", "all"),
    ("faceOption", "gender,age"),
)


def encode_image(image: bytes) -> str:
    """base64 encode an image."""
    return base64.b64encode(image).decode("ascii")


def get_faces(detections: Dict) -> List[Dict]:
    """
    Get the list of the faces.
    """
    faces = []
    for obj in detections["objects"]:
        if not obj["type"] == "face":
            continue
        face = {}
        face["gender"] = obj["attributes"]["gender"]
        face["age"] = obj["attributes"]["age"]
        face["boundingBox"] = obj["boundingBox"]
        faces.append(face)
    return faces


def get_people(detections: Dict) -> List[Dict]:
    """
    Get the list of the people.
    """
    people = []
    for obj in detections["objects"]:
        if not obj["type"] == "person":
            continue
        person = {}
        person["boundingBox"] = obj["boundingBox"]
        people.append(person)
    return people


def get_metadata(detections: Dict) -> Dict:
    """
    Get the detection metadata.
    """
    metadata = {}
    metadata["image_width"] = detections["image"]["width"]
    metadata["image_height"] = detections["image"]["height"]
    metadata["requestId"] = detections["requestId"]
    return metadata


def run_detection(image_encoded: str, api_key: str) -> requests.models.Response:
    """Post an image to Sighthound."""
    headers = {"Content-type": "application/json", "X-Access-Token": api_key}
    try:
        response = requests.post(
            URL_DETECTIONS,
            headers=headers,
            params=DETECTIONS_PARAMS,
            data=json.dumps({"image": image_encoded}),
        )
        return response
    except requests.exceptions.Timeout:
        raise SimplehoundException(f"Timeout connecting to Sighthound")
    except requests.exceptions.ConnectionError as exc:
        raise SimplehoundException(f"Connection error: {exc}")


class SimplehoundException(Exception):
    pass


class API:
    """Work with object detection API."""
