from flask import jsonify, request

from db import db
from models.realm import Realms, realm_schema, realms_schema
from util.reflection import populate_object

def create_realm():
    post_data = request.form if request.form else request.json

    new_realm = Realms.new_realm_obj()

    populate_object(new_realm, post_data)

    db.session.add(new_realm)
    db.session.commit()

    return jsonify({"message": "realm created", "result": realm_schema.dump(new_realm)}), 201

def get_all_realms():
    realms = db.session.query(Realms).all()
    return jsonify({"message": "realms found", "results": realms_schema.dump(realms)}), 200

def get_realm_by_id(realm_id):
    realm = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()

    if not realm:
        return jsonify({"message": "realm does not exist"}), 404
    
    return jsonify({"message": "realm found", "result": realm_schema.dump(realm)}), 200

def update_realm_by_id(realm_id):
    realm = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()
    put_data = request.form if request.form else request.json

    if realm:
        populate_object(realm, put_data)
        db.session.commit()

        return jsonify({"message": "realm updated", "result": realm_schema.dump(realm)}), 200

    return jsonify({"message": "realm does not exist"}), 404

def delete_realm_by_id(realm_id):
    realm = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()

    if not realm:
        return jsonify({"message": "realm does not exist"}), 404

    try:
        db.session.delete(realm)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to delete realm"}), 400

    return jsonify({"message": "realm deleted"}), 200