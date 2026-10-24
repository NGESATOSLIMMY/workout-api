import os
import tempfile

os.environ["DATABASE_URI"] = f"sqlite:///{tempfile.mkdtemp()}/test.db"

import pytest

from server.app import app
from server.config import db


@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def make_exercise(client, name="Squat"):
    return client.post("/exercises", json={"name": name, "category": "strength"})


def make_workout(client):
    return client.post("/workouts", json={"date": "2026-10-24", "duration_minutes": 45})


def test_create_and_list_exercise(client):
    assert make_exercise(client).status_code == 201
    assert len(client.get("/exercises").json) == 1


def test_duplicate_exercise_name_rejected(client):
    make_exercise(client)
    assert make_exercise(client).status_code == 409


def test_schema_validation_exercise(client):
    res = client.post("/exercises", json={"name": "x", "category": "core"})
    assert res.status_code == 422


def test_schema_validation_workout_duration(client):
    res = client.post("/workouts", json={"date": "2026-10-24", "duration_minutes": 0})
    assert res.status_code == 422


def test_add_exercise_to_workout(client):
    w = make_workout(client).json["id"]
    e = make_exercise(client).json["id"]
    res = client.post(f"/workouts/{w}/exercises/{e}/workout_exercises", json={"sets": 3, "reps": 10})
    assert res.status_code == 201
    shown = client.get(f"/workouts/{w}").json
    assert shown["workout_exercises"][0]["exercise"]["name"] == "Squat"


def test_workout_exercise_needs_a_measure(client):
    w = make_workout(client).json["id"]
    e = make_exercise(client).json["id"]
    res = client.post(f"/workouts/{w}/exercises/{e}/workout_exercises", json={})
    assert res.status_code == 422


def test_duplicate_link_rejected(client):
    w = make_workout(client).json["id"]
    e = make_exercise(client).json["id"]
    url = f"/workouts/{w}/exercises/{e}/workout_exercises"
    client.post(url, json={"reps": 5})
    assert client.post(url, json={"reps": 5}).status_code == 409


def test_delete_workout_and_404(client):
    w = make_workout(client).json["id"]
    assert client.delete(f"/workouts/{w}").status_code == 204
    assert client.get(f"/workouts/{w}").status_code == 404


def test_model_validation_raises():
    from server.models import Workout
    with pytest.raises(ValueError):
        Workout(duration_minutes=-5)
