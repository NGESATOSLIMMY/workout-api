from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from server.config import db
from server.models import Exercise
from server.schemas import exercise_schema, exercises_schema

exercises_bp = Blueprint("exercises", __name__, url_prefix="/exercises")


@exercises_bp.get("")
def list_exercises():
    exercises = Exercise.query.order_by(Exercise.name).all()
    return jsonify(exercises_schema.dump(exercises)), 200


@exercises_bp.get("/<int:exercise_id>")
def show_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@exercises_bp.post("")
def create_exercise():
    data = exercise_schema.load(request.get_json() or {})
    exercise = Exercise(**data)
    db.session.add(exercise)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "An exercise with that name already exists"}), 409
    return jsonify(exercise_schema.dump(exercise)), 201


@exercises_bp.delete("/<int:exercise_id>")
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    db.session.delete(exercise)
    db.session.commit()
    return "", 204
