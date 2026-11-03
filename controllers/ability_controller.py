from flask import jsonify, request

from db import db
from models.ability import Abilities, ability_schema, abilities_schema
from util.reflection import populate_object

def create_ability():
    post_data = request.form if request.form else request.json

    new_ability = Abilities.new_ability_obj()

    populate_object(new_ability, post_data)

    db.session.add(new_ability)
    db.session.commit()

    return jsonify({"message": "ability created", "result": ability_schema.dump(new_ability)}), 201

def update_ability_by_id(ability_id):
    ability = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()
    put_data = request.form if request.form else request.json

    if ability:
        populate_object(ability, put_data)
        db.session.commit()
        return jsonify({"message": "ability updated", "result": ability_schema.dump(ability)}), 200

    return jsonify({"message": "ability does not exist"}), 404

def delete_ability_by_id(ability_id):
    ability = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()

    if not ability:
        return jsonify({"message": "ability does not exist"}), 404

    try:
        db.session.delete(ability)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to delete ability"}), 400
    
    return jsonify({"message": "ability deleted"}), 200