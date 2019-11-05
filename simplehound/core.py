"""
Simplehound core.
"""
import base64
import json
from typing import Dict, List

import requests

## Const
HTTP_OK = 200
BAD_API_KEY = 401

## API urls
URL_DETECTIONS_BASE = "https://{}.sighthoundapi.com/v1/detections"
ALLOWED_MODES = ["dev", "prod"]

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


def run_detection(
    image_encoded: str, api_key: str, url_detections: str
) -> requests.models.Response:
    """Post an image to Sighthound."""
    headers = {"Content-type": "application/json", "X-Access-Token": api_key}
    response = requests.post(
        url_detections,
        headers=headers,
        params=DETECTIONS_PARAMS,
        data=json.dumps({"image": image_encoded}),
    )
    return response


class SimplehoundException(Exception):
    pass


class cloud:
    """Work with Sighthound cloud."""

    def __init__(self, api_key: str, mode: str = "dev"):
        if not mode in ALLOWED_MODES:
            raise SimplehoundException(
                f"Mode {mode} is not allowed, must be dev or prod"
            )
        self._api_key = api_key
        self._url_detections = URL_DETECTIONS_BASE.format(mode)

    def detect(self, image: bytes) -> Dict:
        """Run detection on an image (bytes)."""
        response = run_detection(
            encode_image(image), self._api_key, self._url_detections
        )
        if response.status_code == HTTP_OK:
            return response.json()
        elif response.status_code == BAD_API_KEY:
            raise SimplehoundException(f"Bad API key for Sightound")
