from flask import Blueprint

import controllers

ability = Blueprint("ability", __name__)

@ability.route("/ability", methods=["POST"])
def create_ability():
    return controllers.create_ability()

@ability.route("/ability/<ability_id>", methods=["PUT"])
def update_ability_by_id(ability_id):
    return controllers.update_ability_by_id(ability_id)

@ability.route("/ability/delete/<ability_id>", methods=["DELETE"])
def delete_ability_by_id(ability_id):
    return controllers.delete_ability_by_id(ability_id)