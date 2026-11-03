from flask import jsonify, request

from db import db
from models.quest import Quests, quest_schema, quests_schema
from util.reflection import populate_object

def create_quest():
    post_data = request.form if request.form else request.json

    new_quest = Quests.new_quest_obj()

    populate_object(new_quest, post_data)

    db.session.add(new_quest)
    db.session.commit()

    return jsonify({"message": "quest created", "result": quest_schema.dump(new_quest)}), 201


def get_quests_by_difficulty(difficulty):
    quests = db.session.query(Quests).filter(Quests.difficulty == difficulty).all()

    if not quests:
        return jsonify({"message": f"quests with {difficulty} difficulty does not exist"}), 404

    return jsonify({"message": "quests found", "results": quests_schema.dump(quests)}), 200

def get_quest_by_id(quest_id):
    quest = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not quest:
        return jsonify({"message": "quest does not exist"}), 404
    
    return jsonify({"message": "quest found", "result": quest_schema.dump(quest)}), 200

def update_quest_by_id(quest_id):
    quest = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not quest:
        return jsonify({"message": "quest does not exist"}), 404
    
    put_data = request.form if request.form else request.json
    
    populate_object(quest, put_data)
    db.session.commit()

    return jsonify({"message": "quest updated", "result": quest_schema.dump(quest)}), 200

def complete_quest_by_id(quest_id):
    quest = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not quest:
        return jsonify({"message": "quest does not exist"}), 404

    quest.is_completed = not quest.is_completed
    db.session.commit()

    return jsonify({"message": "quest completed", "result": quest_schema.dump(quest)}), 200

def delete_quest_by_id(quest_id):
    quest = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not quest:
        return jsonify({"message": "quest does not exist"}), 404

    try:
        db.session.delete(quest)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to delete quest"}), 400

    return jsonify({"message": "quest deleted"}), 200