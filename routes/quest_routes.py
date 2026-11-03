from flask import Blueprint

import controllers

quest = Blueprint("quest", __name__)

@quest.route("/quest", methods=["POST"])
def create_quest():
    return controllers.create_quest()

@quest.route("/quests/<difficulty_level>", methods=["GET"])
def get_quests_by_difficulty(difficulty_level):
    return controllers.get_quests_by_difficulty(difficulty_level)

@quest.route("/quest/<quest_id>", methods=["GET"])
def get_quest_by_id(quest_id):
    return controllers.get_quest_by_id(quest_id)

@quest.route("/quest/<quest_id>", methods=["PUT"])
def update_quest_by_id(quest_id):
    return controllers.update_quest_by_id(quest_id)

@quest.route("/quest/<quest_id>", methods=["PATCH"])
def complete_quest_by_id(quest_id):
    return controllers.complete_quest_by_id(quest_id)

@quest.route("/quest/delete/<quest_id>", methods=["DELETE"])
def delete_quest_by_id(quest_id):
    return controllers.delete_quest_by_id(quest_id)