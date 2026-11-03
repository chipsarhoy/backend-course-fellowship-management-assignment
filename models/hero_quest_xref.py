from db import db

heroes_quests_association_table = db.Table(
    "HeroesQuestsAssocation",
    db.Model.metadata,
    db.Column("hero_id", db.ForeignKey("Heroes.hero_id", ondelete="CASCADE"), primary_key=True),
    db.Column("quest_id", db.ForeignKey("Quests.quest_id", ondelete="CASCADE"), primary_key=True)
)