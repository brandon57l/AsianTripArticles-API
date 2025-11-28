from flask import Flask
from flask_cors import CORS
from routes import api_blueprint
from db import articles_collection # This ensures db is initialized

def create_app():
    """
    Creates and configures the Flask application.
    """

    app = Flask(__name__)
    CORS(app)

    # Check if the database connection was successful
    if articles_collection is None:
        print("Failed to connect to the database. The application cannot start.")
        # You might want to exit or handle this more gracefully
        exit(1) # Exit the script if no DB connection

    # Register the blueprint with all the API routes
    app.register_blueprint(api_blueprint)

    return app

app = create_app()

if __name__ == '__main__':
    port = 5000

    app.run(port=port, debug=True)
