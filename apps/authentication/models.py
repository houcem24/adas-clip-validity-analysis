# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import joblib
import pandas as pd
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from apps import db, login_manager
from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True)
    email         = db.Column(db.String(64), unique=True)
    password      = db.Column(db.LargeBinary)

    oauth_github  = db.Column(db.String(100), nullable=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

# class Features():
#
#     def __init__(self, maneuver, direction_change, parking_garage, parking_parkout, static_objects, driving_mode,
#                  light_conditions, deviation, artificial_light, dynamic_objects, season, vid_start_frame, vid_start_elv,
#                  vid_start_lat, vid_start_lng, vid_start_tstmp, scn_start_frame, scn_start_elv, scn_start_lat,
#                  scn_start_lng, scn_start_tstmp, vid_end_frame, vid_end_elv, vid_end_lat, vid_end_lng, vid_end_tstmp,
#                  scn_end_frame, scn_end_elv, scn_end_lat, scn_end_lng, scn_end_tstmp):
#         self.maneuver = maneuver
#         self.direction_change = direction_change
#         self.parking_garage = parking_garage
#         self.parking_parkout = parking_parkout
#         self.static_objects = static_objects
#         self.driving_mode = driving_mode
#         self.light_conditions = light_conditions
#         self.deviation = deviation
#         self.artificial_light = artificial_light
#         self.dynamic_objects = dynamic_objects
#         self.season = season
#         self.vid_start_frame = vid_start_frame
#         self.vid_start_elv = vid_start_elv
#         self.vid_start_lat = vid_start_lat
#         self.vid_start_lng = vid_start_lng
#         self.vid_start_tstmp = vid_start_tstmp
#         self.scn_start_frame = scn_start_frame
#         self.scn_start_elv = scn_start_elv
#         self.scn_start_lat = scn_start_lat
#         self.scn_start_lng = scn_start_lng
#         self.scn_start_tstmp = scn_start_tstmp
#         self.vid_end_frame = vid_end_frame
#         self.vid_end_elv = vid_end_elv
#         self.vid_end_lat = vid_end_lat
#         self.vid_end_lng = vid_end_lng
#         self.vid_end_tstmp = vid_end_tstmp
#         self.scn_end_frame = scn_end_frame
#         self.scn_end_elv = scn_end_elv
#         self.scn_end_lat = scn_end_lat
#         self.scn_end_lng = scn_end_lng
#         self.scn_end_tstmp = scn_end_tstmp

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id", ondelete="cascade"), nullable=False)
    user = db.relationship(Users)
