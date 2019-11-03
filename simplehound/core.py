"""
Simplehound core.
"""
import requests
from PIL import Image
from typing import Union, List, Set, Dict

## Const
HTTP_OK = 200
DEFAULT_TIMEOUT = 10  # seconds

## API urls
URL_DETECTIONS = "https://dev.sighthoundapi.com/v1/detections"


def parse_response_body(response: Dict):
    """
    Get a list of the unique objects predicted.
    """
    return None


def post_image(
    url: str, image_bytes: bytes, api_key: str, timeout: int, data: dict = {}
):
    """Post an image to Deepstack."""
    return None


class SimplehoundException(Exception):
    pass


class SimplehoundDetections():
    """Work with object detection API."""
