from flask import jsonify, request

from db import db
from models.race import Races, race_schema, races_schema
from util.reflection import populate_object

def create_race():
    post_data = request.form if request.form else request.json

    new_race = Races.new_race_obj()

    populate_object(new_race, post_data)

    db.session.add(new_race)
    db.session.commit()

    return jsonify({"message": "race created", "result": race_schema.dump(new_race)}), 201

def get_all_races():
    races = db.session.query(Races).all()

    return jsonify({"message": "races found", "results": races_schema.dump(races)}), 200

def get_race_by_id(race_id):
    race = db.session.query(Races).filter(Races.race_id == race_id).first()

    if not race:
        return jsonify({"message": "race does not exist"}), 404

    return jsonify({"message": "race found", "result": race_schema.dump(race)}), 200

def update_race_by_id(race_id):
    race = db.session.query(Races).filter(Races.race_id == race_id).first()
    post_data = request.form if request.form else request.json

    if race:
        populate_object(race, post_data)

        db.session.commit()
        return jsonify({"message": "race updated", "result": race_schema.dump(race)}), 200

    return jsonify({"message": "race does not exist"}), 404

def delete_race_by_id(race_id):
    race = db.session.query(Races).filter(Races.race_id == race_id).first()

    if not race:
        return jsonify({"message": "race does not exist"}), 404

    try:
        db.session.delete(race)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to delete race"}), 400

    return jsonify({"message": "race deleted"}), 200