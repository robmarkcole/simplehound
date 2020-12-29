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
URL_DETECTIONS_BASE = "https://{}.sighthoundapi.com/v1/detections"
URL_RECOGNITIONS_BASE = "https://{}.sighthoundapi.com/v1/recognition?objectType="
ALLOWED_MODES = ["dev", "prod"]

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


def bboxvert_to_tf_style(bbox: Dict, img_width: int, img_height: int) -> Tuple:
    """
    Convert Sighthound bounding box vertices, returned from the recognition API, to tensorflow box style.

    In Tensorflow the bounding box is defined by the tuple (y_min, x_min, y_max, x_max)
    where the coordinates are floats in the range [0.0, 1.0] and
    relative to the width and height of the image.
    For example, if an image is 100 x 200 pixels (height x width) and the bounding
    box is `(0.1, 0.2, 0.5, 0.9)`, the upper-left and bottom-right coordinates of
    the bounding box will be `(40, 10)` to `(180, 50)` (in (x,y) coordinates).
    """

    decimals = 5
    xs = [d["x"] for d in bbox["vertices"]]
    ys = [d["y"] for d in bbox["vertices"]]
    x_min = round(min(xs) / img_width, decimals)
    x_max = round(max(xs) / img_width, decimals)
    y_min = round(min(ys) / img_height, decimals)
    y_max = round(max(ys) / img_height, decimals)
    return (y_min, x_min, y_max, x_max)


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


def get_license_plates(recognitions: Dict) -> List[Dict]:
    """
    Get the list of recognized license plates.
    """
    plates = []
    for obj in recognitions["objects"]:
        if not obj["objectType"] == "licenseplate":
            continue
        annotation = obj["licenseplateAnnotation"]
        attributes = annotation["attributes"]["system"]
        plate = {
            "boundingBox": annotation["bounding"],
            "string": attributes["string"],
            "region": attributes["region"],
        }
        plates.append(plate)
    return plates


def _sighthound_call(
    image_encoded: str, api_key: str, url: str, params=()
) -> requests.models.Response:
    headers = {"Content-type": "application/json", "X-Access-Token": api_key}
    response = requests.post(
        url,
        headers=headers,
        params=params,
        data=json.dumps({"image": image_encoded}),
    )
    return response


def run_detection(
    image_encoded: str, api_key: str, url_detections: str
) -> requests.models.Response:
    """Post an image to Sighthound detection API."""
    return _sighthound_call(image_encoded, api_key, url_detections, DETECTIONS_PARAMS)


def run_recognition(
    image_encoded: str, api_key: str, object_type: str, url_recognitions: str
) -> requests.models.Response:
    """Post an image to Sighthound recognition API."""
    return _sighthound_call(image_encoded, api_key, url_recognitions + object_type)


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
        self._url_recognitions = URL_RECOGNITIONS_BASE.format(mode)

    def detect(self, image: bytes) -> Dict:
        """Run detection on an image (bytes)."""
        response = run_detection(
            encode_image(image), self._api_key, self._url_detections
        )
        if response.status_code == HTTP_OK:
            return response.json()
        elif response.status_code == BAD_API_KEY:
            raise SimplehoundException(f"Bad API key for Sighthound")

    def recognize(self, image: bytes, object_type: str) -> Dict:
        """Run recognition on an image (bytes)."""
        response = run_recognition(
            encode_image(image), self._api_key, object_type, self._url_recognitions
        )
        if response.status_code == HTTP_OK:
            return response.json()
        elif response.status_code == BAD_API_KEY:
            raise SimplehoundException(f"Bad API key for Sighthound")
