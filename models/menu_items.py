from models import db
from models.restaurants import Restaurant
from models.users import User


class MenuItem(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    desc = db.Column(db.String(250))
    price = db.Column(db.String(8))
    course = db.Column(db.String(50))
    restaurant_id = db.Column(db.Integer, db.ForeignKey(Restaurant.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    @property
    def serialize(self):
        return {
            'menu_item_id': self.id,
            'name': self.name,
            'desc': self.desc,
            'price': self.price,
            'course': self.course,
        }

    def __repr__(self):
        return '<MenuItem:{}>'.format(self.name)