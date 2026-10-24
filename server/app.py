from flask import jsonify
from marshmallow import ValidationError

from server.config import create_app
from server.routes import exercises_bp, workouts_bp

app = create_app()
app.register_blueprint(workouts_bp)
app.register_blueprint(exercises_bp)


@app.errorhandler(ValidationError)
def handle_schema_error(err):
    return jsonify({"errors": err.messages}), 422


@app.errorhandler(ValueError)
def handle_model_error(err):
    return jsonify({"error": str(err)}), 422


if __name__ == "__main__":
    app.run(port=5555, debug=True)
