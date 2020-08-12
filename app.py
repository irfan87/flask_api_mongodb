from flask import Flask, request, jsonify, make_response
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, post_load
from bson import ObjectId

app  = Flask(__name__)

app.config['MONGODB_DB'] = 'authors'

db = MongoEngine(app)
ma = Marshmallow(app)

Schema.TYPE_MAPPING[ObjectId] = fields.String

# models
class Author(db.Document):
    name = db.StringField()
    specialization = db.StringField()

# schema
class AuthorsSchema(ma.Schema):
    name = fields.String(required=True)
    specialization = fields.String(required=True)

# routes - GET
@app.route('/authors', methods=['GET'])
def authors_index():
    authors = Author.objects.all()
    # authors_schema = AuthorsSchema(many=True)
    # authors = authors_schema.dump(get_authors)

    # return make_response(jsonify({'authors': authors}), 200)

    return make_response(jsonify({'authors': authors}))

# routes - POST
@app.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    
    author = Author(name=data['name'], specialization=data['specialization'])

    author.save()
    
    author_schema = AuthorsSchema(only=['name', 'specialization'])
    
    author = author_schema.dump(author)
    
    return make_response(jsonify({'author': author}), 201)

# routes - GET[:id]
@app.route('/authors/<id>', methods=['GET'])
def get_author_by_id(id):
    get_author = Author.objects.get_or_404(id=ObjectId(id))

    author_schema = AuthorsSchema()
    
    author = author_schema.dump(get_author)

    return make_response(jsonify({"author": author}))

# routes - PUT[:id]
@app.route('/authors/<id>', methods=['PUT'])
def update_author(id):
    data = request.get_json()
    
    get_author = Author.objects.get(id=ObjectId(id))

    if data.get('specialization'):
        get_author.specialization = data['specialization']
    
    if data.get('name'):
        get_author.name = data['name']

    get_author.save()

    get_author.reload()

    author_schema = AuthorsSchema()

    author = author_schema.dump(get_author)

    return make_response(jsonify({'author': author}))

# routes - DELETE[:id]
@app.route('/authors/<id>', methods=['DELETE'])
def delete_author(id):
    Author.objects(id=ObjectId(id)).delete()

    return make_response('', 204)

if __name__ == '__main__':
    app.run(debug=True)