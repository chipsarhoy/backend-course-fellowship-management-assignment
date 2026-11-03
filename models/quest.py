import marshmallow as ma
import uuid

from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.hero_quest_xref import heroes_quests_association_table

class Quests(db.Model):
    __tablename__ = "Quests"

    quest_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    realm_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Realms.realm_id"), nullable=False)
    quest_name = db.Column(db.String(), nullable=False, unique=True)
    difficulty = db.Column(db.String())
    reward_gold = db.Column(db.Integer())
    is_completed = db.Column(db.Boolean(), default=False)

    realm = db.relationship("Realms", back_populates="quests")
    heroes = db.relationship("Heroes", secondary=heroes_quests_association_table, back_populates="quests")

    def __init__(self, realm_id, quest_name, difficulty=None, reward_gold=None, is_completed=False):
        self.realm_id = realm_id
        self.quest_name = quest_name
        self.difficulty = difficulty
        self.reward_gold = reward_gold
        self.is_completed = is_completed

    def new_quest_obj():
        return Quests("", "", "", 0, False)

class QuestsSchema(ma.Schema):
    class Meta:
        fields = ["quest_id", "quest_name", "difficulty", "reward_gold", "is_completed", "realm", "heroes"]

    quest_id = ma.fields.UUID()
    quest_name = ma.fields.String(required=True)
    difficulty = ma.fields.String(allow_none=True)
    reward_gold = ma.fields.Integer(allow_none=True)
    is_completed = ma.fields.Boolean(dump_default=False)
    realm = ma.fields.Nested("RealmsSchema")
    heroes = ma.fields.Nested("HeroesSchema", many=True, exclude=["quests"])


class MiniQuestsSchema(QuestsSchema):
    heroes = ma.fields.Nested("HeroesSchema", many=True, only=["hero_id", 'hero_name'])
    

quest_schema = QuestsSchema()
quests_schema = QuestsSchema(many=True)
mini_quests_schema = MiniQuestsSchema(many=True)