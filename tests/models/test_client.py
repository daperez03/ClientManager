from unittest.mock import Mock, patch
from pathlib import Path
import pytest
import sys
import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app import create_client
from models.Client import Client


class TestClient:
    def test_create_client_successfully(self):
        session = Mock()
        session.__enter__ = Mock(return_value=session)
        session.__exit__ = Mock(return_value=None)

        with patch("app.Session", return_value=session):
            result = create_client("  Ana Pérez  ", " ana@example.com ", " 8888-8888 ")

        client = session.add.call_args.args[0]

        assert result == "Cliente creado correctamente."
        assert isinstance(client, Client)
        assert client.name == "Ana Pérez"
        assert client.email == "ana@example.com"
        assert client.phone == "8888-8888"
        session.commit.assert_called_once()

    def test_create_client_with_invalid_email(self):
        result = create_client("Ana Pérez", "   ", "8888-8888")

        assert result == "Complete todos los campos."

    def test_create_client_with_missing_fields(self):
        result = create_client("", "ana@example.com", "8888-8888")

        assert result == "Complete todos los campos."