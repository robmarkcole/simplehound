import simplehound.core as hound
import requests
import requests_mock
import pytest


MOCK_BYTES = b"Test"
MOCK_API_KEY = "mock_api_key"
MOCK_TIMEOUT = 8

DETECTIONS = {
    "image": {"width": 960, "height": 480, "orientation": 1},
    "objects": [
        {
            "type": "face",
            "boundingBox": {"x": 305, "y": 151, "height": 28, "width": 30},
            "attributes": {
                "gender": "male",
                "genderConfidence": 0.9733,
                "age": 33,
                "ageConfidence": 0.7801,
                "frontal": True,
            },
        },
        {
            "type": "face",
            "boundingBox": {"x": 855, "y": 147, "height": 29, "width": 24},
            "attributes": {
                "gender": "male",
                "genderConfidence": 0.9834,
                "age": 37,
                "ageConfidence": 0.5096,
                "frontal": False,
            },
        },
        {
            "type": "person",
            "boundingBox": {"x": 227, "y": 133, "height": 245, "width": 125},
        },
        {
            "type": "person",
            "boundingBox": {"x": 833, "y": 137, "height": 268, "width": 93},
        },
    ],
    "requestId": "467f195c4bbf46c69f964b59884dee04",
}

FACES = [
    {
        "boundingBox": {"x": 305, "y": 151, "height": 28, "width": 30},
        "gender": "male",
        "age": 33,
    },
    {
        "boundingBox": {"x": 855, "y": 147, "height": 29, "width": 24},
        "gender": "male",
        "age": 37,
    },
]


def test_get_faces():
    assert hound.get_faces(DETECTIONS) == FACES
