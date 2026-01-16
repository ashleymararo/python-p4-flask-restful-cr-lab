from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/plants', methods=['GET', 'POST'])
def plants():
    if request.method == 'GET':
        plants = Plant.query.all()
        return make_response(jsonify([p.to_dict() for p in plants]), 200)

    elif request.method == 'POST':
        data = request.get_json() # React sends JSON
        new_plant = Plant(
            name=data.get('name'),
            image=data.get('image'),
            price=data.get('price')
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(jsonify(new_plant.to_dict()), 201)

@app.route('/plants/<int:id>', methods=['GET'])
def plant_by_id(id):
    plant = Plant.query.filter_by(id=id).first()
    if not plant:
        return make_response(jsonify({"error": "Plant not found"}), 404)
    return make_response(jsonify(plant.to_dict()), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)