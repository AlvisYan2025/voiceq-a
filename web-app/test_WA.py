# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name
# pylint: disable=unused-import
# pylint: disable=singleton-comparison
# pylint: disable=no-member
# pylint: disable=no-name-in-module

"""import modules"""
import pytest
import pytest_flask
from app import create_app
from db import get_most_recent_transcript


@pytest.fixture
def app():
    """create app"""
    app_instance = create_app()
    app_instance.config["TESTING"] = True
    return app_instance


@pytest.fixture
def client(app):
    """create client"""
    return app.test_client()


def test_index(client):
    """test index page"""
    response = client.get("/")
    assert response.status_code == 200


def test_upload_audio(client):
    """test upload audio function"""
    response = client.get("/upload")
    assert response.status_code == 200


def test_upload_audio_post(client, monkeypatch):
    """test upload audio route"""
    monkeypatch.setattr("app.get_transcript", lambda: "transcript")
    response = client.post(
        "/upload-audio", data={"audio_data": (b"fake_audio_data", "audio.wav")}
    )
    assert response


def test_login(client):
    """test login route"""
    response = client.get("/login")
    assert response.status_code == 200

def test_registration(client):
    """test registration route"""
    response = client.get("/register")
    assert response.status_code == 200

def test_get_ps(client):
    """test get problem set"""
    response = client.get("/ps")
    assert response.status_code == 200
