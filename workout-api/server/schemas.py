from marshmallow import Schema, ValidationError, fields, validate, validates_schema


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=80))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=40))
    equipment_needed = fields.Bool(load_default=False)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=1), allow_none=True)
    sets = fields.Int(validate=validate.Range(min=1), allow_none=True)
    duration_seconds = fields.Int(validate=validate.Range(min=1), allow_none=True)
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates_schema
    def require_a_measure(self, data, **kwargs):
        if not any(data.get(f) for f in ("reps", "sets", "duration_seconds")):
            raise ValidationError(
                "Provide at least one of reps, sets, or duration_seconds.", "_schema"
            )

    @validates_schema
    def sets_need_reps(self, data, **kwargs):
        if data.get("sets") and not data.get("reps"):
            raise ValidationError("'sets' requires 'reps'.", "sets")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=600))
    notes = fields.Str(validate=validate.Length(max=500), allow_none=True)
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
