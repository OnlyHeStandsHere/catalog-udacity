from flask import Blueprint, render_template, url_for, redirect, request, flash
from models.restaurants import Restaurant, db
from flask import session as login_session

# make a restaurant blueprint
restaurant = Blueprint('restaurant', __name__)


# index to display all restaurants
# only dispaly the CRUD version of the webpage if users are logged in
# otherwise we serve a read only version of the page
@restaurant.route('/restaurants/')
def index():
    restaurants = Restaurant.query.all()
    user_id = login_session.get('id')
    if user_id:
        return render_template("restaurant/index.html", restaurants=restaurants)
    else:
        return render_template("restaurant/logged_out_index.html", restaurants=restaurants)


# creates a new restaurant and serves the form to do so
# upon successful creation redirect to index, otherwise
# flash the error and re-render the form template
@restaurant.route("/restaurant/new/", methods=['GET', 'POST'])
def create():
    user_id = login_session.get('id')
    if user_id:
        if request.method == 'GET':
            return render_template("restaurant/form.html", restaurant='')
        elif request.method == 'POST':
            rest_name = request.form.get("restaurant_name")
            if rest_name:
                new_restaurant = Restaurant(name=rest_name, user_id=login_session.get('id'))
                db.session.add(new_restaurant)
                db.session.commit()
                return redirect(url_for("restaurant.index"))
            else:
                flash("Please enter a valid restaurant name")
                return render_template("restaurant/form.html", restaurant='')
        else:
            flash("Invalid Submission, please try again")
            return render_template("restaurant/form.html", restaurant='')
    else:
        flash("operation not allowed. Please log in to create a restaurant")
        return redirect(url_for('restaurant.index'))


# Updates the name of an existing restaurant
# if the restaurant cannot be found, we'll flash an error and re-render the form
@restaurant.route("/restaurant/<int:restaurant_id>/edit/", methods=['GET', 'POST'])
def update(restaurant_id):
    user_id = login_session.get('id')
    current_restaurant = Restaurant.query.get(restaurant_id)
    if user_id:
        if current_restaurant:
            if request.method == "GET":
                return render_template("restaurant/form.html", restaurant=current_restaurant)
            elif request.method == "POST":
                name = request.form.get("restaurant_name")
                if name:
                    current_restaurant.name = name
                    db.session.add(current_restaurant)
                    db.session.commit()
                    flash("Restaurant has been updated to {}".format(current_restaurant.name))
                    return redirect(url_for('restaurant.index'))
            else:
                flash("Invalid Request, please try again")
                return render_template("restaurant/form.html", restaurant='')
        else:
            flash("The restaurant could not be found. Please try again")
            return render_template("restaurant/form.html", restaurant='')
    else:
        flash("operation not allowed. Please log in to update a restaurant")
        return redirect(url_for('restaurant.index'))


# route to delete a restaurant
# only allow the delete if a user is logged in
@restaurant.route("/restaurant/<int:restaurant_id>/delete/", methods=['GET', 'POST'])
def delete(restaurant_id):
    current_restaurant = Restaurant.query.get(restaurant_id)
    user_id = login_session.get('id')
    if user_id:
        if current_restaurant:
            if request.method == "GET":
                return render_template("restaurant/delete.html", restaurant=current_restaurant)
            elif request.method == 'POST':
                db.session.delete(current_restaurant)
                db.session.commit()
                flash("Restaurant Deleted Successfully!")
                return redirect(url_for("restaurant.index"))
            else:
                flash("Invalid Request, please try again")
                return render_template("restaurant/delete.html", restaurant='')
        else:
            flash("Restaurant not found, please try again")
            return render_template("restaurant/delete.html", restaurant='')
    else:
        flash("operation not allowed please log in to delete a restaurant item")
        return redirect(url_for('restaurant.index'))


@restaurant.route("/restaurant/<int:restaurant_id>/menu")
def show_menu(restaurant_id):
    current_restaurant = Restaurant.query.get(restaurant_id)
    user_id = login_session.get('id')
    if current_restaurant:
        if user_id:
            return render_template("restaurant/menu.html", restaurant=current_restaurant)
        else:
            return render_template("restaurant/logged_out_menu.html", restaurant=current_restaurant)
    else:
        flash("Restaurant not found. Please try again")
        return render_template("restaurant/index.html", restaurant='')

