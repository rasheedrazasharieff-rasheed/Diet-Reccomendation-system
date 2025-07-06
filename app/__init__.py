from flask import Flask, render_template_string
from flask_cors import CORS
import os


def create_app():
    # Get the absolute path to the project root directory
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Create the Flask app with correct template and static folder paths
    app = Flask(__name__,
                template_folder=os.path.join(project_dir, 'templates'),
                static_folder=os.path.join(project_dir, 'static'))
    CORS(app)

    # Configure the secret key for session management
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_development')

    # Configure session to use filesystem
    app.config['SESSION_TYPE'] = 'filesystem'

    # Increase session lifetime
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

    # Enable session debugging
    app.config['DEBUG'] = True

    # Print the template folder path for debugging
    print(f"Template folder path: {app.template_folder}")
    print(f"Static folder path: {app.static_folder}")

    # Check if important templates exist
    template_files = [
        'diet/form.html',
        'diet/processing.html',
        'diet/meal_plan.html',
        'diet/error.html'
    ]

    for template in template_files:
        template_path = os.path.join(app.template_folder, template)
        exists = os.path.exists(template_path)
        print(f"Template {template}: {'EXISTS' if exists else 'MISSING'} at {template_path}")

    # Register blueprints
    from app.routes import main
    from app.auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app

