"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from distutils.command.upload import upload

import os
from click import option
from app import app, db, login_manager
from flask import render_template, request, redirect, send_from_directory, url_for, flash,session
from flask_login import login_user, logout_user, current_user, login_required
# from app.forms import LoginForm
from app.models import UserProfile, Property
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from app.forms import PropertiesForm, PropertyType
from . import db
import locale
locale.setlocale( locale.LC_ALL, 'en_CA.UTF-8' ) 


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/properties')
def properties():
    """Renders a display of all the Properties"""
    fetched_properties = Property.query.all()

    return render_template('properties.html',properties = fetched_properties,locale = locale)
    


@app.route('/properties/create', methods=["GET", "POST"])
def add_property():
    """Renders the add property form"""
    form = PropertiesForm()
    form.propType.choices = [(option.value,option.name) for option in PropertyType]


    if request.method == "POST":
        if form.validate():
            print("validated")
            title = form.title.data
            bedrooms = form.bedrooms.data
            bathrooms  = form.bathrooms.data
            location = form.location.data
            price = form.price.data
            type = form.propType.data
            description = form.description.data
            photo = form.photo.data
            if photo.filename == '':
                flash('No selected Photo')
                print("No selected Photo")
                return redirect(request.url)
            
            photoname = secure_filename(photo.filename)
            # print(photoname)
            # print(f"retirived title:{title},bedrooms:{bedrooms}, bathrooms:{bathrooms}, location:{location},type:{type}, descrip: {description}, price:{price}")
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'],photoname))

            property = Property(title,bedrooms,bathrooms,location,price,PropertyType(type),description,photoname)
            db.session.add(property)
            db.session.commit()

            flash("Property Added",'success')
            return redirect(url_for('properties'))
        else:
            print(form.errors)
    # else:      
    #     flash_errors(form)
    #     return redirect(request.url)


    return render_template('new_property.html',form = form) 

@app.route('/uploads/<filename>')
def get_image(filename):
    try:
        return send_from_directory(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER']),filename)
    except FileNotFoundError:
        return "https://via.placeholder.com/150"

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        # change this to actually validate the entire form submission
        # and not just one field
        if form.validate_on_submit():
            # Get the username and password values from the form.
            email = form.email.data
            password = form.password.data

            # using your model, query database for a user based on the username
            # and password submitted. Remember you need to compare the password hash.
            # You will need to import the appropriate function to do so.
            # Then store the result of that query to a `user` variable so it can be
            # passed to the login_user() method below.

            user = UserProfile.query.filter_by(email=email).first()

            if user is not None and check_password_hash(user.password,password):
                # get user id, load into session
                login_user(user)
                flash("Logged in successfully",'success')

                return redirect(url_for("secure_page"))  # they should be redirected to a secure-page route instead
            else:
                flash('Username or Password is incorrect.', 'danger')
        flash_errors(form)
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have Logged out.','success')
    return redirect(url_for("home"))  



# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
