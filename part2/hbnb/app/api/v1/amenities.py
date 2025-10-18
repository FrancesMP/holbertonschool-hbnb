from flask_restx import Namespace, Resource, fields
from hbnb.app.services.facade import HBnBFacade
from hbnb.app.models.amenity import Amenity

# Create namespace for amenities
api = Namespace('amenities', description='Amenity operations')

# Connect to business logic
facade = HBnBFacade()

# Define the data structure for amenities
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Amenity name')
})

# Handle /api/v1/amenities/ (create and list)
@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    def post(self):
        """Create a new amenity"""
        data = api.payload
        try:
            amenity = Amenity(name=data['name'])
            facade.amenity_repo.add(amenity)
            return amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
    
    def get(self):
        """Get all amenities"""
        amenities = facade.amenity_repo.get_all()
        return [amenity.to_dict() for amenity in amenities], 200

# Handle /api/v1/amenities/<amenity_id> (get one and update)
@api.route('/<amenity_id>')
class AmenityResource(Resource):
    def get(self, amenity_id):
        """Get a specific amenity by ID"""
        amenity = facade.amenity_repo.get(amenity_id)
        if amenity:
            return amenity.to_dict(), 200
        return {'error': 'Amenity not found'}, 404
    
    @api.expect(amenity_model)
    def put(self, amenity_id):
        """Update an amenity"""
        data = api.payload
        amenity = facade.amenity_repo.get(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        try:
            amenity.update(data)
            return amenity.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
