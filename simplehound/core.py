"""
Simplehound core.
"""
import base64
import json
from typing import Dict, List, Set, Union

import requests

## Const
HTTP_OK = 200

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
    response = requests.post(
        URL_DETECTIONS,
        headers=headers,
        params=DETECTIONS_PARAMS,
        data=json.dumps({"image": image_encoded}),
    )
    return response


class SimplehoundException(Exception):
    pass


class cloud:
    """Work with Sighthound cloud."""

    def __init__(
        self, api_key: str,
    ):
        self._api_key = api_key

    def detect(self, image: bytes) -> Dict:
        """Run detection on an image (bytes)."""
        try:
            response = run_detection(encode_image(image), self._api_key)
            if not response.status_code == HTTP_OK:
                raise SimplehoundException(
                    f"Sightound error - response code: {response.status_code}, reason: {response.reason}"
                )
            return response.json()
        except Exception as exc:
            SimplehoundException(str(exc))
