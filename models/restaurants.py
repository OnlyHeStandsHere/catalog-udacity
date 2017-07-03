from models import db
from models.users import User

class Restaurant(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    menu_items = db.relationship("MenuItem", backref="restaurant")
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def serialize_menu_items(self):
        return {
            "restaurant_id": self.id,
            "name": self.name,
            "menu_items": [i.name for i in self.menu_items]
        }

    @property
    def serialize(self):
        return {
            "restaurant_id": self.id,
            "name": self.name
        }

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return '<Restaurant:{}>'.format(self.name)
