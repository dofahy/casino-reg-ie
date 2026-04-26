import os

import pytest
from dotenv import load_dotenv

from regulate_ie.db import Base, get_engine
from regulate_ie.main import app, init_app

load_dotenv()
os.environ["DB_NAME"] = "regulate_ie_test"
init_app()


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=get_engine())
    with app.test_client() as client:
        yield client
    Base.metadata.drop_all(bind=get_engine())


def test_ingest_and_get(client):
    res = client.post(
        "/ingest", json={"source": "regulation.com", "content": "important information"}
    )
    assert res.status_code == 200
    id = res.json["id"]
    res = client.get("/regulations")
    assert res.status_code == 200
    assert any(r["id"] == id for r in res.json)
    res = client.delete(f"/regulations/{id}")
    assert res.status_code == 200
