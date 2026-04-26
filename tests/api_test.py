from dotenv import load_dotenv

load_dotenv()
import os

os.environ['DB_NAME'] = 'regulate_ie_test'
import pytest

from regulate_ie.db import Base, engine
from regulate_ie.main import app


@pytest.fixture(scope='module')
def client():
    Base.metadata.create_all(bind=engine)
    with app.test_client() as client:
        yield client
    Base.metadata.drop_all(bind=engine)


def test_ingest_and_get(client):
    res = client.post(
        '/ingest', json={'source': 'regulation.com', 'content': 'important information'}
    )
    assert res.status_code == 200
    id = res.json['id']
    res = client.get('/regulations')
    assert res.status_code == 200
    assert any(r['id'] == id for r in res.json)
    res = client.delete(f"/regulations/{id}")
    assert res.status_code == 200
