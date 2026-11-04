from unittest.mock import Mock, patch
from pathlib import Path
import pytest
import sys
import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app import create_client, read_clients, update_client, delete_client
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

    def test_read_clients_returns_all_clients(self):
        session = Mock()
        session.__enter__ = Mock(return_value=session)
        session.__exit__ = Mock(return_value=None)
        session.query.return_value.order_by.return_value.all.return_value = [
            Client(id=1, name="Ana Pérez", email="ana@example.com", phone="8888-8888"),
            Client(id=2, name="Luis Gómez", email="luis@example.com", phone="7777-7777"),
        ]

        with patch("app.Session", return_value=session):
            result = read_clients()

        assert result == [
            {"id": 1, "name": "Ana Pérez", "email": "ana@example.com", "phone": "8888-8888"},
            {"id": 2, "name": "Luis Gómez", "email": "luis@example.com", "phone": "7777-7777"},
        ]

    def test_read_clients_filters_by_search_term(self):
        session = Mock()
        session.__enter__ = Mock(return_value=session)
        session.__exit__ = Mock(return_value=None)
        query = Mock()
        query.filter.return_value.order_by.return_value.all.return_value = [
            Client(id=1, name="Ana Pérez", email="ana@example.com", phone="8888-8888"),
        ]
        session.query.return_value = query

        with patch("app.Session", return_value=session):
            result = read_clients("ana")

        assert result == [
            {"id": 1, "name": "Ana Pérez", "email": "ana@example.com", "phone": "8888-8888"},
        ]
    def test_delete_client_successfully(self):
        session = Mock()
        session.__enter__ = Mock(return_value=session)
        session.__exit__ = Mock(return_value=None)

        client = Client(
            id=1,
            name="Ana Pérez",
            email="ana@example.com",
            phone="8888-8888"
        )
        session.get.return_value = client

        with patch("app.Session", return_value=session):
            result = delete_client(1, True)

        assert result == "Cliente eliminado correctamente."
        session.get.assert_called_once_with(Client, 1)
        session.delete.assert_called_once_with(client)
        session.commit.assert_called_once()

    def test_delete_client_not_found(self):
        session = Mock()
        session.__enter__ = Mock(return_value=session)
        session.__exit__ = Mock(return_value=None)
        session.get.return_value = None

        with patch("app.Session", return_value=session):
            result = delete_client(99, True)

        assert result == "Cliente no encontrado."
        session.delete.assert_not_called()
        session.commit.assert_not_called()

    def test_delete_client_without_confirmation(self):
        result = delete_client(1, False)

        assert result == "Debe confirmar la eliminación."