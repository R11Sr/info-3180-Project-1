from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,SelectField,IntegerField,FloatField
from wtforms.validators import InputRequired,DataRequired,NumberRange
from flask_wtf.file import FileField,FileAllowed,FileRequired

from app.models import PropertyType


class PropertiesForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])

    description = TextAreaField('description',validators=[DataRequired()])

    bedrooms = IntegerField('bedrooms', validators=[NumberRange(min = 0,max=775,message =f"Number of rooms cannot exceed {max} or be less than{min}"),DataRequired()])

    bathrooms = IntegerField('bathrooms', validators=[NumberRange(min = 0,max=775,message =f"Number of bathrooms cannot exceed {max} or be less than{min}"),DataRequired()])

    price = FloatField('price',validators=[NumberRange(min = 0,max=9999999999,message =f"Number of bathrooms cannot exceed {max} or be less than{min}"),DataRequired()])

    propType = SelectField('type',validators=[DataRequired()])

    location = StringField('location',validators=[DataRequired()])

    photo = FileField('photo',validators=[FileRequired(),FileAllowed(['jpg', 'png','jpeg'],'Select Image Files only.')])
