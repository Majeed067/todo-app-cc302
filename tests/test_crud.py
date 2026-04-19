import pytest
from app import app, db, Todo

@pytest.fixture
def client():
    app.config["TESTING"] = True
    # Use in-memory DB for tests
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client

def test_create_task(client):
    # CREATE
    resp = client.post("/add", data={"title": "Buy milk"}, follow_redirects=True)
    assert resp.status_code == 200

    # READ/VERIFY
    page = resp.get_data(as_text=True)
    assert "Buy milk" in page

def test_update_task_fail(client):
    # Intentional failure for assignment
    assert 0  # <- This will fail on purpose

def test_update_task(client):
    # CREATE first
    resp_create = client.post("/add", data={"title": "Old title"}, follow_redirects=True)
    assert resp_create.status_code == 200

    # Get task ID dynamically
    task = Todo.query.first()
    task_id = task.id

    # UPDATE
    task.title = "New title"
    db.session.commit()

    # READ/VERIFY
    resp = client.get("/")
    assert "New title" in resp.get_data(as_text=True)

def test_delete_task(client):
    # CREATE first
    client.post("/add", data={"title": "To be deleted"}, follow_redirects=True)

    # Get task ID dynamically
    task = Todo.query.filter_by(title="To be deleted").first()
    task_id = task.id

    # DELETE
    client.get(f"/delete/{task_id}", follow_redirects=True)

    # READ/VERIFY
    resp = client.get("/")
    page = resp.get_data(as_text=True)
    assert "To be deleted" not in page