"""
Simplehound core.
"""
import base64
from typing import Dict, List, Set, Union

import requests
from PIL import Image

## Const
HTTP_OK = 200
DEFAULT_TIMEOUT = 10  # seconds

## API urls
URL_DETECTIONS = "https://dev.sighthoundapi.com/v1/detections"


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


def run_detection(image_base64: str, api_key: str):
    """Post an image to Sighthound."""
    return None


class SimplehoundException(Exception):
    pass


class API:
    """Work with object detection API."""
