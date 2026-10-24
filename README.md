# Workout Tracker API

A Flask + SQLAlchemy + Marshmallow backend for a workout tracking app used by personal trainers.

## Description

Trainers can create workouts and reusable exercises, then attach exercises to workouts with
sets, reps, or a duration. Exercises are reusable across many workouts through a join model
(`WorkoutExercise`), which stores the per-workout details.

**Models:** `Exercise`, `Workout`, `WorkoutExercise` (join model with extra columns)

**Validations**
- Table constraints: unique exercise name, CHECK on name length, workout duration > 0, reps/sets/duration > 0, unique (workout, exercise) pair
- Model validations (`@validates`): name length, category required, positive duration/reps/sets, notes length
- Schema validations (Marshmallow): field length/range rules, at least one of reps/sets/duration required, `sets` requires `reps`

## Project structure

    server/
      app.py          app creation, blueprint registration, error handlers
      config.py       Flask app factory, db and migrate objects
      models.py       SQLAlchemy models and model validations
      schemas.py      Marshmallow schemas and schema validations
      routes/
        workouts.py   workout endpoints + add exercise to workout
        exercises.py  exercise endpoints
      seed.py         example data
      test_app.py     tests

## Installation

    pipenv install --dev
    pipenv shell
    export FLASK_APP=server/app.py
    flask db upgrade
    python -m server.seed

## Run

    flask run --port 5555

## Tests

    pytest server/test_app.py

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/workouts` | List all workouts with their exercises |
| GET | `/workouts/<id>` | Show one workout (404 if missing) |
| POST | `/workouts` | Create a workout. Body: `date` (YYYY-MM-DD), `duration_minutes`, optional `notes` |
| DELETE | `/workouts/<id>` | Delete a workout and its exercise links |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Show one exercise (404 if missing) |
| POST | `/exercises` | Create an exercise. Body: `name`, `category`, optional `equipment_needed` |
| DELETE | `/exercises/<id>` | Delete an exercise and its workout links |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout. Body: any of `sets`, `reps`, `duration_seconds` (at least one) |

Status codes: 201 created, 204 deleted, 404 not found, 409 duplicate, 422 validation error.

## Example

    curl -X POST localhost:5555/workouts/1/exercises/2/workout_exercises \
      -H "Content-Type: application/json" -d '{"sets": 3, "reps": 12}'
