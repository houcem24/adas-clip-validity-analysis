# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, SubmitField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])

#Form Features Validator
# class CreateFeaturesForm(FlaskForm):
#     maneuver = StringField('Maneuver', validators=[DataRequired()])
#     direction_change = StringField('Direction Change', validators=[DataRequired()])
#     parking_garage = StringField('Parking Garage', validators=[DataRequired()])
#     parking_parkout = StringField('Parking Parkout', validators=[DataRequired()])
#     static_objects = StringField('Static Objects', validators=[DataRequired()])
#     driving_mode = StringField('Driving Mode', validators=[DataRequired()])
#     light_conditions = StringField('Light Conditions', validators=[DataRequired()])
#     deviation = StringField('Deviation', validators=[DataRequired()])
#     artificial_light = StringField('Artificial Light', validators=[DataRequired()])
#     dynamic_objects = StringField('Dynamic Objects', validators=[DataRequired()])
#     season = StringField('Season', validators=[DataRequired()])
#     vid_start_frame = IntegerField('VID_START_FRAME', validators=[DataRequired()])
#     vid_start_elv = FloatField('VID_START_ELV', validators=[DataRequired()])
#     vid_start_lat = FloatField('VID_START_LAT', validators=[DataRequired()])
#     vid_start_lng = FloatField('VID_START_LNG', validators=[DataRequired()])
#     vid_start_tstmp = IntegerField('VID_START_TSTMP', validators=[DataRequired()])
#     scn_start_frame = IntegerField('SCN_START_FRAME', validators=[DataRequired()])
#     scn_start_elv = FloatField('SCN_START_ELV', validators=[DataRequired()])
#     scn_start_lat = FloatField('SCN_START_LAT', validators=[DataRequired()])
#     scn_start_lng = FloatField('SCN_START_LNG', validators=[DataRequired()])
#     scn_start_tstmp = IntegerField('SCN_START_TSTMP', validators=[DataRequired()])
#     vid_end_frame = IntegerField('VID_END_FRAME', validators=[DataRequired()])
#     vid_end_elv = FloatField('VID_END_ELV', validators=[DataRequired()])
#     vid_end_lat = FloatField('VID_END_LAT', validators=[DataRequired()])
#     vid_end_lng = FloatField('VID_END_LNG', validators=[DataRequired()])
#     vid_end_tstmp = IntegerField('VID_END_TSTMP', validators=[DataRequired()])
#     scn_end_frame = IntegerField('SCN_END_FRAME', validators=[DataRequired()])
#     scn_end_elv = FloatField('SCN_END_ELV', validators=[DataRequired()])
#     scn_end_lat = FloatField('SCN_END_LAT', validators=[DataRequired()])
#     scn_end_lng = FloatField('SCN_END_LNG', validators=[DataRequired()])
#     scn_end_tstmp = IntegerField('SCN_END_TSTMP', validators=[DataRequired()])
#     submit = SubmitField('Submit')


