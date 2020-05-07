"""
Simplehound core.
"""
import base64
import json
from typing import Dict, List, Tuple

import requests

## Const
HTTP_OK = 200
BAD_API_KEY = 401

## API urls
URL_DETECTIONS_BASE = "https://{}.sighthoundapi.com/v1/{}"
ALLOWED_MODES = ["dev", "prod"]
ALLOWED_ENDPOINTS = ["detections","recognition"]

RECOGNITION_PARAMS = (
    ("objectType", "licenseplate"),
#    ("faceOption", "gender,age"),
)

DETECTIONS_PARAMS = (
    ("type", "all"),
    ("faceOption", "gender,age"),
)


def bbox_to_tf_style(bbox: Dict, img_width: int, img_height: int) -> Tuple:
    """
    Convert Sighthound bounding box to tensorflow box style.
    
    In Tensorflow the bounding box is defined by the tuple (y_min, x_min, y_max, x_max)
    where the coordinates are floats in the range [0.0, 1.0] and
    relative to the width and height of the image.
    For example, if an image is 100 x 200 pixels (height x width) and the bounding
    box is `(0.1, 0.2, 0.5, 0.9)`, the upper-left and bottom-right coordinates of
    the bounding box will be `(40, 10)` to `(180, 50)` (in (x,y) coordinates).
    """

    decimals = 5
    x_min = round(bbox["x"] / img_width, decimals)
    x_max = round((bbox["x"] + bbox["width"]) / img_width, decimals)
    y_min = round(bbox["y"] / img_height, decimals)
    y_max = round((bbox["y"] + bbox["height"]) / img_height, decimals)
    return (y_min, x_min, y_max, x_max)


def encode_image(image: bytes) -> str:
    """base64 encode an image."""
    return base64.b64encode(image).decode("ascii")

def get_licensePlates(detections: Dict) -> List[Dict]:
    """
    Get the list of the faces.
    """
    licensePlates = []
    for obj in detections["objects"]:
        if not obj["objectType"] == "licenseplate":
            continue
        plate = {}
        plate["name"] = obj["licenseplateAnnotation"]["attributes"]["system"]["string"]["name"]
        plate["confidence"] = obj["licenseplateAnnotation"]["attributes"]["system"]["string"]["confidence"]
#        plate["boundingBox"] = obj["licenseplateAnnotation"]["bounding"]["system"]["vertices"]
        licensePlates.append(plate)
    return licensePlates

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


def run_detection(
    image_encoded: str, api_key: str, url_detections: str, url_params
) -> requests.models.Response:
    """Post an image to Sighthound."""
    headers = {"Content-type": "application/json", "X-Access-Token": api_key}
    response = requests.post(
        url_detections,
        headers=headers,
        params=url_params,
        data=json.dumps({"image": image_encoded})
    )
    return response


class SimplehoundException(Exception):
    pass


class cloud:
    """Work with Sighthound cloud."""

    def __init__(self, api_key: str, mode: str = "dev", endpoint: str = "recognition"):
        if not mode in ALLOWED_MODES:
            raise SimplehoundException(
                f"Mode {mode} is not allowed, must be dev or prod"
            )
        if not endpoint in ALLOWED_ENDPOINTS:
            raise SimplehoundException(
                f"Endpoint {endpoint} is not allowed, must be recognition or detections"
            )
        self._api_key = api_key
        self._url_detections = URL_DETECTIONS_BASE.format(mode,endpoint)
        self._url_params = DETECTIONS_PARAMS if endpoint == "detections" else RECOGNITION_PARAMS 

    def detect(self, image: bytes) -> Dict:
        """Run detection on an image (bytes)."""
        response = run_detection(
            encode_image(image), self._api_key, self._url_detections, self._url_params
        )
        if response.status_code == HTTP_OK:
            return response.json()
        elif response.status_code == BAD_API_KEY:
            raise SimplehoundException(f"Bad API key for Sightound")