from datetime import date, timedelta
import pytest

from fastapi_sqlmodel_security.data_store import SqlModelDataStore

CONNECTION_URLS = [
    "sqlite:///./test.db",
    # "postgresql+psycopg://user:pass@localhost:5432/postgres",
]


def _get_data_store(conn_url: str) -> SqlModelDataStore:
    return SqlModelDataStore(conn_url)


def test_database_creation():
    pass


@pytest.mark.parametrize("conn_url", CONNECTION_URLS)
def test_create_key(conn_url: str):
    data_store = _get_data_store(conn_url)
    key = data_store.create_key("test_key", False)
    assert key is not None

    return key


@pytest.mark.parametrize("conn_url", CONNECTION_URLS)
def test_revoke_key(conn_url: str):
    data_store = _get_data_store(conn_url)

    key = test_create_key(conn_url)

    result = data_store.revoke_key(key)
    assert result is True


@pytest.mark.parametrize("conn_url", CONNECTION_URLS)
def test_renew_key(conn_url: str):
    data_store = _get_data_store(conn_url)

    key = test_create_key(conn_url)

    result = data_store.renew_key(key, date.today() + timedelta(days=1))
    assert result is True


@pytest.mark.parametrize("conn_url", CONNECTION_URLS)
@pytest.mark.skip(reason="To be fixed with a fixture")
def test_get_usage_stats(conn_url: str):
    data_store = _get_data_store(conn_url)
    count = 10

    keys = []
    for _ in range(count):
        keys.append(test_create_key(conn_url))

    stats = data_store.get_usage_stats()
    assert stats is not None
    assert len(stats) == count