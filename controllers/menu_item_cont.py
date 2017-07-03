from flask import Blueprint, flash, render_template, url_for, request, redirect
from models.menu_items import MenuItem, Restaurant, db
from flask import session as login_session

# create a blueprint for all menu items
menu_items = Blueprint("menu_item", __name__)


# route to create a menu item for a given restaurant
# we only allow creation of an item if a user is currently logged in
# if this route gets a post request, we'll store the submitted form data in the DB
@menu_items.route("/restaurant/<int:restaurant_id>/menu/new", methods=['GET', 'POST'])
def create(restaurant_id):
    user_id = login_session.get('id')
    restaurant = Restaurant.query.get(restaurant_id)
    if user_id:
        if request.method == 'POST':
            restaurant = Restaurant.query.get(restaurant_id)
            name = request.form.get("name")
            desc = request.form.get("desc")
            price = request.form.get("price")
            menu_item = MenuItem(name=name, desc=desc, price=price, restaurant_id=restaurant.id)
            db.session.add(menu_item)
            db.session.commit()
            flash("Menu item added successfully!")
            return redirect(url_for("restaurant.show_menu", restaurant_id=restaurant.id))
        else:
            return render_template("menu/form.html", menu_item='', restaurant=restaurant)
    else:
        flash('Operation not allowed. Please log in to create a menu item')
        return redirect(url_for('restaurant.index'))


# updates a menu item for a given restaurant
# only performs the update when a POST is received on this route
# if we have a get request, then we'll render the same form as used for the create route
# we only perform an operation if the menu_item exists. This prevents users trying random urls
# as the id's are in plain views
@menu_items.route("/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/edit", methods=['GET', 'POST'])
def update(restaurant_id, menu_item_id):
    restaurant = Restaurant.query.get(restaurant_id)
    menu_item = MenuItem.query.get(menu_item_id)
    user_id = login_session.get('id')
    if user_id:
        if menu_item:
            if request.method == 'GET':
                return render_template("menu/form.html", menu_item=menu_item, restaurant=restaurant)
            elif request.method == 'POST':
                menu_item.name = request.form.get("name")
                menu_item.desc = request.form.get("desc")
                menu_item.price = request.form.get("price")
                db.session.add(menu_item)
                db.session.commit()
                flash("Menu item updated successfully!")
                return redirect(url_for("restaurant.show_menu", restaurant_id=menu_item.restaurant.id))
            else:
                flash("Invalid Action, Please try again")
                return redirect(url_for("restaurant.menu", restaurant_id=menu_item.restaurant.id))
        else:
            flash("Item not found, please try again")
            return redirect(url_for("restaurant.index"))
    else:
        flash('Operation not allowed. Please log in to create a menu item')
        return redirect(url_for('restaurant.index'))


# remove a menu item for a given restaurant
# we only remove an item if a user if currently logged in
# We also only remove an item if it exists, otherwise we tell the user to try again
# this prevents users messing with the url and trying random requests.
@menu_items.route("/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/delete", methods=['GET', 'POST'])
def delete(restaurant_id, menu_item_id):
    restaurant = Restaurant.query.get(restaurant_id)
    menu_item = MenuItem.query.get(menu_item_id)
    user_id = login_session.get('id')
    if user_id:
        if menu_item:
            if request.method == "GET":
                return render_template("menu/delete.html", menu_item=menu_item)
            elif request.method == "POST":
                db.session.delete(menu_item)
                db.session.commit()
                flash("Menu item successfully deleted!")
                return redirect(url_for("restaurant.show_menu", restaurant_id=restaurant.id))
            else:
                flash("Invalid operation. Please try again")
                return redirect(url_for("restaurant.show_menu", restaurant_id=restaurant.id))
        else:
            flash("Menu item not found. Please try again")
            return redirect(url_for("restaurant.show_menu", restaurant_id=restaurant.id))
    else:
        flash('Operation not allowed. Please log in to create a menu item')
        return redirect(url_for('restaurant.index'))

