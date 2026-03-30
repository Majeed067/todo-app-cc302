import pytest
from app import app, db, Todo

@pytest.fixture
def client():
    # Arrange
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # in-memory DB for testing
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.test_client() as client:
        # Create all tables before tests
        with app.app_context():
            db.create_all()
        yield client
        # Drop tables after tests
        with app.app_context():
            db.drop_all()

def test_create_task(client):
    # Act
    resp = client.post("/add", data={"title": "Buy milk"}, follow_redirects=True)
    # Assert
    assert resp.status_code == 200
    assert "Buy milk" in resp.get_data(as_text=True)

def test_update_task(client):
    # Arrange
    client.post("/add", data={"title": "Old title"}, follow_redirects=True)

    # Act
    resp = client.post("/update/1", data={"title": "New title"}, follow_redirects=True)
    # Assert
    assert resp.status_code == 200
    page = resp.get_data(as_text=True)
    assert "New title" in page
    assert "Old title" not in page

def test_delete_task(client):
    # Arrange
    client.post("/add", data={"title": "To be deleted"}, follow_redirects=True)

    # Act
    resp = client.get("/delete/1", follow_redirects=True)
    # Assert
    assert resp.status_code == 200
    page = resp.get_data(as_text=True)
    assert "To be deleted" not in page