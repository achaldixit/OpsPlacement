from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField , SubmitField, RadioField, SelectField , DecimalField  
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import InputRequired, Email, Length , NumberRange, Regexp , EqualTo

# from wtforms.fields.html5 import EmailField
# from wtforms.widgets import TextArea

class  PropertyForm(FlaskForm):
    City = SelectField('City', choices=[('','---------Select---------'),(1,'Mumbai'),(2,'Delhi NCR'),(3,'Bangalore')],validators=[InputRequired()])
    inflationFactor = DecimalField('Inflation Factor ', validators=[  NumberRange(min=0.7,max=1.3,message="Enter Correct Inflation Factor")],default=1 )
    Capacity = DecimalField('Per Square Feet Capacity ',default=5)
    TruckCost = DecimalField('Vehical Cost Per Hour',default=235)

