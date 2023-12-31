from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def dictify(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record

@app.route("/random", methods=['GET']) # type: ignore
def random():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = choice(all_cafes)
    # return jsonify(
    #     cafe = {
    #         # "id": random_cafe.id,
    #         "name": random_cafe.name,
    #         "img_url": random_cafe.img_url,
    #         "location": random_cafe.location,
    #         "map_url": random_cafe.map_url,   
    #         "amenities": {
    #             "can_take_calls": random_cafe.can_take_calls,
    #             "has_sockets": random_cafe.has_sockets,
    #             "has_toilet": random_cafe.has_toilet,
    #             "has_wifi": random_cafe.has_wifi,
    #             "seats": random_cafe.seats,
    #             "coffee_price": random_cafe.coffee_price
    #         }
    #         }
    #     )
    return jsonify(cafe=random_cafe.dictify()), 200

@app.route("/all", methods=['GET']) # type: ignore
def all():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return jsonify(cafes=[cafe.dictify() for cafe in all_cafes]), 200

@app.route("/search", methods=['GET']) # type: ignore
def search():
    all_cafes = db.session.execute(db.select(Cafe).where(Cafe.location==request.args.get("loc"))).scalars().all()
    if len(all_cafes) == 0:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location"}), 404
    elif len(all_cafes) == 1:
        return jsonify(cafe=all_cafes[0].dictify()), 200
    else:
        return jsonify(cafes=[cafe.dictify() for cafe in all_cafes]), 200

## HTTP POST - Create Record

@app.route("/add", methods=['POST']) # type: ignore
def add():
    new_cafe = Cafe(
        name = request.form["name"],
        img_url = request.form["img_url"],
        location = request.form["location"],
        map_url = request.form["map_url"],   
        can_take_calls = bool(request.form["can_take_calls"]),
        has_sockets = bool(request.form["has_sockets"]),
        has_toilet = bool(request.form["has_toilet"]),
        has_wifi = bool(request.form["has_wifi"]),
        seats = request.form["seats"],
        coffee_price = request.form["coffee_price"]
        )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe"}), 201

## HTTP PUT/PATCH - Update Record

@app.route("/update-price/<int:cafe_id>", methods=['PATCH']) # type: ignore
def update_price(cafe_id):
    try:
        cafe_to_update = db.get_or_404(Cafe, cafe_id)
    except:
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database"}), 404
    else:
        cafe_to_update.coffee_price = request.args.get("coffee_price")
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price"}), 200

## HTTP DELETE - Delete Record

@app.route("/report-closed/<int:cafe_id>", methods=['DELETE']) # type: ignore
def report_closed(cafe_id):
    if request.args.get("api-key") == "TopSecretAPIKey":
        try:
            cafe_to_delete = db.get_or_404(Cafe, cafe_id) 
        except:
            return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database"}), 404
        else:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe"}), 200
    else:
        return jsonify(error={"Not Allowed": "Sorry, that's not allowed. Make sure you have the correct api-key"}), 403
    

if __name__ == '__main__':
    app.run(debug=True)
