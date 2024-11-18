from http import HTTPStatus

import pytest
from flask.testing import FlaskClient

from src.poc.app import app


class TestApi:

    @pytest.fixture(scope='session', name="test_client")
    def fixture_test_client(self) -> FlaskClient:
        with app.test_client() as test_client:
            yield test_client

    def test_root(self, test_client):
        response = test_client.get('/')

        assert response.status_code == HTTPStatus.OK
