from flask import Blueprint

import controllers

hero = Blueprint("hero", __name__)

@hero.route("/hero", methods=["POST"])
def create_hero():
    return controllers.create_hero()

@hero.route("/hero-quest", methods=["POST"])
def create_hero_quest():
    return controllers.create_hero_quest()

@hero.route("/heroes", methods=["GET"])
def get_all_heroes():
    return controllers.get_all_heroes()

@hero.route("/heroes/alive", methods=["GET"])
def get_living_heroes():
    return controllers.get_living_heroes()

@hero.route("/hero/<hero_id>", methods=["GET"])
def get_hero_by_id(hero_id):
    return controllers.get_hero_by_id(hero_id)

@hero.route("/hero/<hero_id>/quests", methods=["GET"])
def get_quests_by_hero(hero_id):
    return controllers.get_quests_by_hero(hero_id)

@hero.route("/hero/<hero_id>", methods=["PUT"])
def update_hero_by_id(hero_id):
    return controllers.update_hero_by_id(hero_id)

@hero.route("/hero/delete/<hero_id>", methods=["DELETE"])
def delete_hero_by_id(hero_id):
    return controllers.delete_hero_by_id(hero_id)