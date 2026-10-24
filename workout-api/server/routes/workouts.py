from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from server.config import db
from server.models import Exercise, Workout, WorkoutExercise
from server.schemas import (
    workout_exercise_schema,
    workout_schema,
    workouts_schema,
)

workouts_bp = Blueprint("workouts", __name__, url_prefix="/workouts")


@workouts_bp.get("")
def list_workouts():
    workouts = Workout.query.order_by(Workout.date).all()
    return jsonify(workouts_schema.dump(workouts)), 200


@workouts_bp.get("/<int:workout_id>")
def show_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify(workout_schema.dump(workout)), 200


@workouts_bp.post("")
def create_workout():
    data = workout_schema.load(request.get_json() or {})
    workout = Workout(**data)
    db.session.add(workout)
    db.session.commit()
    return jsonify(workout_schema.dump(workout)), 201


@workouts_bp.delete("/<int:workout_id>")
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    db.session.delete(workout)
    db.session.commit()
    return "", 204


@workouts_bp.post("/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
def add_exercise_to_workout(workout_id, exercise_id):
    if not db.session.get(Workout, workout_id):
        return jsonify({"error": "Workout not found"}), 404
    if not db.session.get(Exercise, exercise_id):
        return jsonify({"error": "Exercise not found"}), 404

    data = workout_exercise_schema.load(request.get_json() or {})
    link = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
    db.session.add(link)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "That exercise is already in this workout"}), 409
    return jsonify(workout_exercise_schema.dump(link)), 201
