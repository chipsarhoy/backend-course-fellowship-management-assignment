import marshmallow as ma
import uuid

from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.hero_quest_xref import heroes_quests_association_table

class Heroes(db.Model):
    __tablename__ = "Heroes"

    hero_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    race_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Races.race_id"), nullable=False)
    hero_name = db.Column(db.String(), nullable=False, unique=True)
    age = db.Column(db.Integer())
    health_points = db.Column(db.Integer())
    is_alive = db.Column(db.Boolean(), default=True)

    race = db.relationship("Races", back_populates="heroes")
    abilities = db.relationship("Abilities", back_populates="hero", cascade="all, delete-orphan")
    quests = db.relationship("Quests", secondary=heroes_quests_association_table, back_populates="heroes")

    def __init__(self, race_id, hero_name, age=None, health_points=None, is_alive=True):
        self.race_id = race_id
        self.hero_name = hero_name
        self.age = age
        self.health_points = health_points
        self.is_alive = is_alive

    def new_hero_obj():
        return Heroes("", "", 0, 0, True)

class HeroesSchema(ma.Schema):
    class Meta:
        fields = ["hero_id", "hero_name", "age", "health_points", "is_alive", "race", "abilities", "quests"]

    hero_id = ma.fields.UUID()
    hero_name = ma.fields.String(required=True)
    age = ma.fields.Integer(allow_none=True)
    health_points = ma.fields.Integer(allow_none=True)
    is_alive = ma.fields.Boolean(dump_default=True)
    race = ma.fields.Nested('RacesSchema', exclude=["heroes"])
    abilities = ma.fields.Nested("AbilitiesSchema", many=True, exclude=["hero"])
    quests = ma.fields.Nested("QuestsSchema", many=True, exclude=["heroes"])

hero_schema = HeroesSchema()
heroes_schema = HeroesSchema(many=True)