#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'



@app.before_first_request
def seed_data_if_empty():
    if not Bakery.query.first():

        bakery1 = Bakery(name="Delightful donuts")
        bakery2 = Bakery(name="Incredible crullers")

        db.session.add_all([bakery1, bakery2])
        db.session.commit()

        goods = [
            BakedGood(name="Chocolate dipped donut", price=2.75, bakery_id=bakery1.id),
            BakedGood(name="Apple-spice filled donut", price=3.5, bakery_id=bakery1.id),
            BakedGood(name="Glazed honey cruller", price=3.25, bakery_id=bakery2.id),
            BakedGood(name="Chocolate cruller", price=3.4, bakery_id=bakery2.id),
        ]

        db.session.add_all(goods)
        db.session.commit()




@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    return jsonify([b.to_dict() for b in bakeries]), 200


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)

    if not bakery:
        return make_response(jsonify({"error": "Bakery not found"}), 404)

    return make_response(
        jsonify(bakery.to_dict(rules=('baked_goods',))),
        200
    )


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()

    return make_response(
        jsonify([good.to_dict() for good in baked_goods]),
        200
    )


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()

    return make_response(jsonify(baked_good.to_dict()), 200)



if __name__ == '__main__':
    app.run(port=5555, debug=True)
