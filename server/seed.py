from datetime import date

from server.app import app
from server.config import db
from server.models import Exercise, Workout, WorkoutExercise

with app.app_context():
    print("Clearing tables...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding exercises...")
    squat = Exercise(name="Back Squat", category="strength", equipment_needed=True)
    pushup = Exercise(name="Push-up", category="strength", equipment_needed=False)
    plank = Exercise(name="Plank", category="core", equipment_needed=False)
    run = Exercise(name="Treadmill Run", category="cardio", equipment_needed=True)
    db.session.add_all([squat, pushup, plank, run])

    print("Seeding workouts...")
    w1 = Workout(date=date(2026, 10, 19), duration_minutes=60, notes="Leg day")
    w2 = Workout(date=date(2026, 10, 21), duration_minutes=45, notes="Upper body + core")
    w3 = Workout(date=date(2026, 10, 23), duration_minutes=30)
    db.session.add_all([w1, w2, w3])
    db.session.commit()

    print("Linking exercises to workouts...")
    db.session.add_all([
        WorkoutExercise(workout_id=w1.id, exercise_id=squat.id, sets=4, reps=8),
        WorkoutExercise(workout_id=w1.id, exercise_id=plank.id, duration_seconds=60),
        WorkoutExercise(workout_id=w2.id, exercise_id=pushup.id, sets=3, reps=15),
        WorkoutExercise(workout_id=w2.id, exercise_id=plank.id, duration_seconds=90),
        WorkoutExercise(workout_id=w3.id, exercise_id=run.id, duration_seconds=1200),
    ])
    db.session.commit()
    print("Done!")
