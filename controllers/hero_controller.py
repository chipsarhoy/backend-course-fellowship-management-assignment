from flask import jsonify, request

from db import db
from models.hero import Heroes, hero_schema, heroes_schema
from models.quest import Quests, mini_quests_schema
from util.reflection import populate_object

def create_hero():
    post_data = request.form if request.form else request.json

    new_hero = Heroes.new_hero_obj()

    populate_object(new_hero, post_data)

    db.session.add(new_hero)
    db.session.commit()

    return jsonify({"message": "hero created", "result": hero_schema.dump(new_hero)}), 201

def create_hero_quest():
    post_data = request.form if request.form else request.json
    hero_id = post_data.get("hero_id")
    quest_id = post_data.get("quest_id")

    hero_query = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()
    quest_query = db.session.query(Quests).filter(Quests.quest_id == quest_id).first()

    if not hero_query:
        return jsonify({"message": "hero does not exist"}), 404
    
    if not quest_query:
        return jsonify({"message": "quest does not exist"}), 404
    
    quest_query.heroes.append(hero_query)
    db.session.commit()
    
    return jsonify({"message": "hero added to quest", "result": hero_schema.dump(hero_query)}), 200

def get_all_heroes():
    heroes = db.session.query(Heroes).all()

    return jsonify({"message": "heroes found", "results": heroes_schema.dump(heroes)}), 200

def get_living_heroes():
    heroes = db.session.query(Heroes).filter(Heroes.is_alive == True).all()

    return jsonify({"message": "heroes found", "results": heroes_schema.dump(heroes)}), 200

def get_hero_by_id(hero_id):
    hero = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()

    if not hero:
        return jsonify({"message": "hero does not exist"}), 404

    return jsonify({"message": "hero found", "result": hero_schema.dump(hero)}), 200

def get_quests_by_hero(hero_id):
    hero = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()

    if not hero:
        return jsonify({"message": "hero does not exist"}), 404

    return jsonify({"message": "quests found", "results": mini_quests_schema.dump(hero.quests)}), 200

def update_hero_by_id(hero_id):
    hero = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()

    if not hero:
        return jsonify({"message": "hero does not exist"}), 404

    put_data = request.form if request.form else request.json

    populate_object(hero, put_data)

    db.session.commit()
    return jsonify({"message": "hero updated", "result": hero_schema.dump(hero)}), 200

def delete_hero_by_id(hero_id):
    hero = db.session.query(Heroes).filter(Heroes.hero_id == hero_id).first()

    if not hero:
        return jsonify({"message": "hero does not exist"}), 404

    try:
        db.session.delete(hero)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to delete hero"}), 400

    return jsonify({"message": "hero deleted"}), 200