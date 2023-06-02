from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
# from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cards.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
print(basedir)
# DB objektas
class Card(db.Model):
    __tablename__ = 'Card'
    id = db.Column(db.Integer, primary_key=True)
    frontSide = db.Column("FrontSide", db.String)
    backSide = db.Column("BackSide", db.String)
    # modified = db.Column(db.DateTime, default=datetime.utcnow)


# Užduoties schema
class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'frontSide', 'backSide')

card_schema = CardSchema()
cards_schema = CardSchema(many=True)



# Crud
@app.route('/cards', methods=['POST'])
def create_card():
    # db.create_all()
    frontSide = request.json['frontSide']
    backSide = request.json['backSide']
    new_card = Card(frontSide =frontSide , backSide=backSide)
    db.session.add(new_card)
    db.session.commit()
    return card_schema.jsonify(new_card)

# cRud
@app.route('/cards', methods=['GET'])
def get_cards():
    all_cards = Card.query.all()
    result = cards_schema.dump(all_cards)
    return jsonify(result)

# cRud
@app.route('/cards/<id>', methods=['GET'])
def get_card(id):
    card = Card.query.get(id)
    return card_schema.jsonify(card)

# crUd
@app.route('/cards/<id>', methods=['PUT'])
def edit_card(id):
    card = Card.query.get(id)
    card.frontSide = request.json['frontSide']
    card.backSide = request.json['backSide']
    db.session.commit()
    return card_schema.jsonify(card)

# cruD
@app.route('/cards/<id>', methods=['DELETE'])
def delete_card(id):
    card = Card.query.get(id)
    db.session.delete(card)
    db.session.commit()
    return card_schema.jsonify(card)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=8024, debug=True)