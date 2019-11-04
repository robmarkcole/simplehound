import simplehound.core as hound
import requests
import requests_mock
import pytest


MOCK_BYTES = b"Test"
MOCK_API_KEY = "mock_api_key"

B64_ENCODED_BYTES = "VGVzdA=="

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

PEOPLE = [
    {"boundingBox": {"x": 227, "y": 133, "height": 245, "width": 125}},
    {"boundingBox": {"x": 833, "y": 137, "height": 268, "width": 93}},
]

METADATA = {
    "image_width": 960,
    "image_height": 480,
    "requestId": "467f195c4bbf46c69f964b59884dee04",
}


def test_encode_image():
    assert hound.encode_image(MOCK_BYTES) == B64_ENCODED_BYTES


def test_get_faces():
    assert hound.get_faces(DETECTIONS) == FACES


def test_get_people():
    assert hound.get_people(DETECTIONS) == PEOPLE


def test_get_metadata():
    assert hound.get_metadata(DETECTIONS) == METADATA


def test_good_run_detection():
    with requests_mock.Mocker() as mock_req:
        mock_req.post(hound.URL_DETECTIONS, status_code=hound.HTTP_OK, json=DETECTIONS)
        response = hound.run_detection(B64_ENCODED_BYTES, MOCK_API_KEY)
        assert response.json() == DETECTIONS
