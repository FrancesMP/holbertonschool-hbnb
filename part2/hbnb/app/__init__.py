from flask import Flask
from flask_restx import Api, Resource

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews, and amenities will be added later
    @app.route('/')
    def index():
        return "Welcome to HBNB API 🚀"
    
    @api.route('/hello')
    class HelloResource(Resource):
        def get(self):
            return {"message": "Hello from HBNB API 🚀"}

    return app