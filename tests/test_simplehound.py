import pytest
import requests
import requests_mock

import simplehound.core as hound

MOCK_API_KEY = "mock_api_key"
MOCK_BYTES = b"Test"
B64_ENCODED_MOCK_BYTES = "VGVzdA=="
URL_DETECTIONS_DEV = hound.URL_DETECTIONS_BASE.format("dev")
URL_DETECTIONS_PROD = hound.URL_DETECTIONS_BASE.format("prod")

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
    assert hound.encode_image(MOCK_BYTES) == B64_ENCODED_MOCK_BYTES


def test_get_faces():
    assert hound.get_faces(DETECTIONS) == FACES


def test_get_people():
    assert hound.get_people(DETECTIONS) == PEOPLE


def test_get_metadata():
    assert hound.get_metadata(DETECTIONS) == METADATA


def test_good_run_detection():
    with requests_mock.Mocker() as mock_req:
        mock_req.post(URL_DETECTIONS_DEV, status_code=hound.HTTP_OK, json=DETECTIONS)
        response = hound.run_detection(
            B64_ENCODED_MOCK_BYTES, MOCK_API_KEY, URL_DETECTIONS_DEV
        )
        assert response.json() == DETECTIONS


def test_cloud_init():
    """Test that the dev or prod url are being set correctly."""
    api_dev = hound.cloud(MOCK_API_KEY)
    assert api_dev._url_detections == URL_DETECTIONS_DEV

    api_prod = hound.cloud(MOCK_API_KEY, mode="prod")
    assert api_prod._url_detections == URL_DETECTIONS_PROD

    with pytest.raises(hound.SimplehoundException) as exc:
        hound.cloud(MOCK_API_KEY, mode="bad")
    assert str(exc.value) == "Mode bad is not allowed, must be dev or prod"


def test_cloud_detect_good():
    with requests_mock.Mocker() as mock_req:
        mock_req.post(URL_DETECTIONS_DEV, status_code=hound.HTTP_OK, json=DETECTIONS)
        api = hound.cloud(MOCK_API_KEY)
        detections = api.detect(MOCK_BYTES)
        assert detections == DETECTIONS


def test_cloud_detect_bad_key():
    with pytest.raises(
        hound.SimplehoundException
    ) as exc, requests_mock.Mocker() as mock_req:
        mock_req.post(
            URL_DETECTIONS_DEV, status_code=hound.BAD_API_KEY, json=DETECTIONS
        )
        api = hound.cloud(MOCK_API_KEY)
        detections = api.detect(MOCK_BYTES)
    assert str(exc.value) == "Bad API key for Sightound"
