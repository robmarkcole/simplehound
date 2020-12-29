import pytest
import requests
import requests_mock

import simplehound.core as hound

MOCK_API_KEY = "mock_api_key"
MOCK_BYTES = b"Test"
B64_ENCODED_MOCK_BYTES = "VGVzdA=="
URL_DETECTIONS_DEV = hound.URL_DETECTIONS_BASE.format("dev")
URL_DETECTIONS_PROD = hound.URL_DETECTIONS_BASE.format("prod")
URL_RECOGNITIONS_DEV = hound.URL_RECOGNITIONS_BASE.format("dev")
URL_RECOGNITIONS_PROD = hound.URL_RECOGNITIONS_BASE.format("prod")

## RAW API RESPONSES
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


RECOGNITIONS_LICENSEPLATE = {
    "image": {"width": 960, "height": 480, "orientation": 1},
    "objects": [
        {
            "objectType": "licenseplate",
            "licenseplateAnnotation": {
                "bounding": {
                    "vertices": [
                        {"x": 494, "y": 294},
                        {"x": 542, "y": 294},
                        {"x": 542, "y": 318},
                        {"x": 494, "y": 318},
                    ]
                },
                "attributes": {
                    "system": {
                        "string": {"name": "7XJT316", "confidence": 0.116},
                        "characters": [
                            {
                                "bounding": {
                                    "vertices": [
                                        {"y": 303, "x": 502},
                                        {"y": 303, "x": 507},
                                        {"y": 313, "x": 507},
                                        {"y": 313, "x": 502},
                                    ]
                                },
                                "index": 0,
                                "confidence": 0.9186,
                                "character": "7",
                            },
                            {
                                "bounding": {
                                    "vertices": [
                                        {"y": 302, "x": 507},
                                        {"y": 302, "x": 512},
                                        {"y": 313, "x": 512},
                                        {"y": 313, "x": 507},
                                    ]
                                },
                                "index": 1,
                                "confidence": 0.8351,
                                "character": "X",
                            },
                            {
                                "bounding": {
                                    "vertices": [
                                        {"y": 302, "x": 511},
                                        {"y": 302, "x": 516},
                                        {"y": 313, "x": 516},
                                        {"y": 313, "x": 511},
                                    ]
                                },
                                "index": 2,
                                "confidence": 0.8033,
                                "character": "J",
                            },
                            {
                                "bounding": {
                                    "vertices": [
                                        {"y": 302, "x": 516},
                                        {"y": 302, "x": 521},
                                        {"y": 313, "x": 521},
                                        {"y": 313, "x": 516},
                                    ]
                                },
                                "index": 3,
                                "confidence": 0.8243,
                                "character": "T",
                            },
                            {
                                "bounding": {
                                    "vertices": [
                                        {"y": 303, "x": 521},
                                        {"y": 303, "x": 526},
                                        {"y": 313, "x": 526},
                                        {"y": 313, "x": 521},
                                    ]
                                },
                                "index": 4,
                                "confidence": 0.8527,
                                "character": "3",
                            },
                            {
                                "bounding": {
                                    "vertices": [
                                        {"y": 302, "x": 525},
                                        {"y": 302, "x": 530},
                                        {"y": 313, "x": 530},
                                        {"y": 313, "x": 525},
                                    ]
                                },
                                "index": 5,
                                "confidence": 0.3805,
                                "character": "1",
                            },
                            {
                                "bounding": {
                                    "vertices": [
                                        {"y": 302, "x": 530},
                                        {"y": 302, "x": 535},
                                        {"y": 313, "x": 535},
                                        {"y": 313, "x": 530},
                                    ]
                                },
                                "index": 6,
                                "confidence": 0.7038,
                                "character": "6",
                            },
                        ],
                        "region": {"name": "California", "confidence": 0.9918},
                    }
                },
            },
        }
    ],
    "requestId": "467f195c4bbf46c69f964b59884dee04",
}

RECOGNITIONS_VEHICLES = {
    "image": {"width": 1080, "height": 675, "orientation": 1},
    "requestId": "7b09bdf1547441c78fcd336ac1b78077",
    "objects": [
        {
            "objectId": "_vehicle_c3b12324-1f19-4606-90c6-39c25c8c39fb",
            "vehicleAnnotation": {
                "bounding": {
                    "vertices": [
                        {"x": 289, "y": 150},
                        {"x": 1036, "y": 150},
                        {"x": 1036, "y": 602},
                        {"x": 289, "y": 602},
                    ]
                },
                "recognitionConfidence": 0.8554,
                "attributes": {
                    "system": {
                        "make": {"name": "Ford", "confidence": 0.8554},
                        "model": {"name": "Ranger", "confidence": 0.8554},
                        "color": {"name": "black", "confidence": 0.9988},
                        "vehicleType": "car",
                    }
                },
            },
            "objectType": "vehicle",
        }
    ],
}

RECOGNITIONS_ALL = {
    "image": {"width": 1080, "height": 675, "orientation": 1},
    "requestId": "a14d1d7e426a429d960fa100d2351cdb",
    "objects": [
        {
            "objectId": "_vehicle_c3b12324-1f19-4606-90c6-39c25c8c39fb",
            "vehicleAnnotation": {
                "bounding": {
                    "vertices": [
                        {"x": 289, "y": 150},
                        {"x": 1036, "y": 150},
                        {"x": 1036, "y": 602},
                        {"x": 289, "y": 602},
                    ]
                },
                "recognitionConfidence": 0.8554,
                "licenseplate": {
                    "bounding": {
                        "vertices": [
                            {"x": 755, "y": 377},
                            {"x": 914, "y": 377},
                            {"x": 914, "y": 419},
                            {"x": 755, "y": 419},
                        ]
                    },
                    "attributes": {
                        "system": {
                            "string": {"name": "CV67CBU", "confidence": 0.4044},
                            "characters": [
                                {
                                    "bounding": {
                                        "vertices": [
                                            {"y": 385, "x": 778},
                                            {"y": 385, "x": 794},
                                            {"y": 413, "x": 794},
                                            {"y": 413, "x": 778},
                                        ]
                                    },
                                    "index": 0,
                                    "confidence": 0.9797,
                                    "character": "C",
                                },
                                {
                                    "bounding": {
                                        "vertices": [
                                            {"y": 384, "x": 796},
                                            {"y": 384, "x": 812},
                                            {"y": 412, "x": 812},
                                            {"y": 412, "x": 796},
                                        ]
                                    },
                                    "index": 1,
                                    "confidence": 0.985,
                                    "character": "V",
                                },
                                {
                                    "bounding": {
                                        "vertices": [
                                            {"y": 384, "x": 812},
                                            {"y": 384, "x": 829},
                                            {"y": 412, "x": 829},
                                            {"y": 412, "x": 812},
                                        ]
                                    },
                                    "index": 2,
                                    "confidence": 0.4732,
                                    "character": "6",
                                },
                                {
                                    "bounding": {
                                        "vertices": [
                                            {"y": 383, "x": 830},
                                            {"y": 383, "x": 846},
                                            {"y": 411, "x": 846},
                                            {"y": 411, "x": 830},
                                        ]
                                    },
                                    "index": 3,
                                    "confidence": 0.9895,
                                    "character": "7",
                                },
                                {
                                    "bounding": {
                                        "vertices": [
                                            {"y": 383, "x": 853},
                                            {"y": 383, "x": 869},
                                            {"y": 411, "x": 869},
                                            {"y": 411, "x": 853},
                                        ]
                                    },
                                    "index": 4,
                                    "confidence": 0.998,
                                    "character": "C",
                                },
                                {
                                    "bounding": {
                                        "vertices": [
                                            {"y": 382, "x": 869},
                                            {"y": 382, "x": 886},
                                            {"y": 410, "x": 886},
                                            {"y": 410, "x": 869},
                                        ]
                                    },
                                    "index": 5,
                                    "confidence": 0.9933,
                                    "character": "B",
                                },
                                {
                                    "bounding": {
                                        "vertices": [
                                            {"y": 381, "x": 887},
                                            {"y": 381, "x": 903},
                                            {"y": 410, "x": 903},
                                            {"y": 410, "x": 887},
                                        ]
                                    },
                                    "index": 6,
                                    "confidence": 0.9026,
                                    "character": "U",
                                },
                            ],
                            "region": {"name": "UK", "confidence": 0.9972},
                        }
                    },
                },
                "attributes": {
                    "system": {
                        "make": {"name": "Ford", "confidence": 0.8554},
                        "model": {"name": "Ranger", "confidence": 0.8554},
                        "color": {"name": "black", "confidence": 0.9988},
                        "vehicleType": "car",
                    }
                },
            },
            "objectType": "vehicle",
        }
    ],
}

## Processed responses
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

LICENSEPLATE_PROCESSED = [
    {
        "boundingBox": {
            "vertices": [
                {"x": 494, "y": 294},
                {"x": 542, "y": 294},
                {"x": 542, "y": 318},
                {"x": 494, "y": 318},
            ]
        },
        "string": {"name": "7XJT316", "confidence": 0.116},
        "region": {"name": "California", "confidence": 0.9918},
    }
]

VEHICLES_PROCESSED = [
    {
        "boundingBox": {
            "vertices": [
                {"x": 289, "y": 150},
                {"x": 1036, "y": 150},
                {"x": 1036, "y": 602},
                {"x": 289, "y": 602},
            ]
        },
        "recognitionConfidence": 0.8554,
        "vehicleType": "car",
        "make": "Ford",
        "model": "Ranger",
        "color": "black",
        "licenseplate": "unknown",
        "region": "unknown",
    }
]

ALL_PROCESSED = [
    {
        "boundingBox": {
            "vertices": [
                {"x": 289, "y": 150},
                {"x": 1036, "y": 150},
                {"x": 1036, "y": 602},
                {"x": 289, "y": 602},
            ]
        },
        "recognitionConfidence": 0.8554,
        "vehicleType": "car",
        "make": "Ford",
        "model": "Ranger",
        "color": "black",
        "licenseplate": "CV67CBU",
        "region": "UK",
    }
]


def test_bbox_to_tf_style():
    bbox = {"x": 227, "y": 133, "height": 245, "width": 125}
    img_width = 960
    img_height = 480
    assert hound.bbox_to_tf_style(bbox, img_width, img_height) == (
        0.27708,
        0.23646,
        0.7875,
        0.36667,
    )


def test_bboxvert_to_tf_style():
    bbox = RECOGNITIONS_LICENSEPLATE["objects"][0]["licenseplateAnnotation"]["bounding"]
    img_width = 960
    img_height = 480
    assert hound.bboxvert_to_tf_style(bbox, img_width, img_height) == (
        0.6125,
        0.51458,
        0.6625,
        0.56458,
    )


def test_encode_image():
    assert hound.encode_image(MOCK_BYTES) == B64_ENCODED_MOCK_BYTES


def test_get_license_plates():
    assert hound.get_license_plates(RECOGNITIONS_LICENSEPLATE) == LICENSEPLATE_PROCESSED


def test_get_vehicles():
    assert hound.get_vehicles(RECOGNITIONS_VEHICLES) == VEHICLES_PROCESSED
    assert hound.get_vehicles(RECOGNITIONS_ALL) == ALL_PROCESSED


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
        assert response == DETECTIONS


def test_good_run_recognition():
    with requests_mock.Mocker() as mock_req:
        mock_req.post(
            URL_RECOGNITIONS_DEV + "licenseplate",
            status_code=hound.HTTP_OK,
            json=RECOGNITIONS_LICENSEPLATE,
        )
        response = hound.run_recognition(
            B64_ENCODED_MOCK_BYTES,
            MOCK_API_KEY,
            URL_RECOGNITIONS_DEV,
            "licenseplate",
        )
        assert response == RECOGNITIONS_LICENSEPLATE


def test_cloud_init():
    """Test that the dev or prod url are being set correctly."""
    api_dev = hound.cloud(MOCK_API_KEY)
    assert api_dev._url_detections == URL_DETECTIONS_DEV
    assert api_dev._url_recognitions == URL_RECOGNITIONS_DEV

    api_prod = hound.cloud(MOCK_API_KEY, mode="prod")
    assert api_prod._url_detections == URL_DETECTIONS_PROD
    assert api_prod._url_recognitions == URL_RECOGNITIONS_PROD

    with pytest.raises(hound.SimplehoundException) as exc:
        hound.cloud(MOCK_API_KEY, mode="bad")
    assert str(exc.value) == "Mode bad is not allowed, must be dev or prod"


def test_cloud_detect_good():
    with requests_mock.Mocker() as mock_req:
        mock_req.post(URL_DETECTIONS_DEV, status_code=hound.HTTP_OK, json=DETECTIONS)
        api = hound.cloud(MOCK_API_KEY)
        detections = api.detect(MOCK_BYTES)
        assert detections == DETECTIONS


def test_cloud_recognize_licenseplate_good():
    with requests_mock.Mocker() as mock_req:
        mock_req.post(
            URL_RECOGNITIONS_DEV + "licenseplate",
            status_code=hound.HTTP_OK,
            json=RECOGNITIONS_LICENSEPLATE,
        )
        api = hound.cloud(MOCK_API_KEY)
        recognitions = api.recognize(MOCK_BYTES, "licenseplate")
        assert recognitions == RECOGNITIONS_LICENSEPLATE


def test_cloud_detect_bad_key():
    with pytest.raises(
        hound.SimplehoundException
    ) as exc, requests_mock.Mocker() as mock_req:
        mock_req.post(
            URL_DETECTIONS_DEV, status_code=hound.BAD_API_KEY, json=DETECTIONS
        )
        api = hound.cloud(MOCK_API_KEY)
        detections = api.detect(MOCK_BYTES)
    assert str(exc.value) == "Bad API key for Sighthound"
