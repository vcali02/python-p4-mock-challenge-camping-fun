from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    #attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #relationships
    #An Activity has many Signups
    signups_of_cur_activity = db.relationship('Signup', back_populates= 'activity')
    #activity = db.relationship('Activity', back_populates= 'signups_of_cur_activity')


    #association_proxys
    #An Activity has many Campers through Signups
    campers_of_cur_activity = association_proxy('signups_of_cur_activity', 'camper')


    #serializer_rules
    #-relationship that exist in current model.bidirectional relationsip in associated model
    serialize_rules = ('-signups_of_cur_activity.camper', '-campers_of_cur_activity.activities_of_cur_camper', '-signups_of_cur_activity.activity')
    #serializer_rules = ('-signups_of_cur_activity', '-campers_of_cur_activity.camper')

    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'





class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    #attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #relationships
    #A Camper has many Signups
    signups_of_cur_camper = db.relationship('Signup', back_populates = 'camper')


    #association_proxy
    #A Camper has many Activitys through Signups
    activities_of_cur_camper = association_proxy('signups_of_cur_camper', 'activity')

    #serializer_rules
    serialize_rules = ('-signups_of_cur_camper.camper', '-activities_of_cur_camper.activity')


    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'

    #VALIDATIONS
    #must have a name
    @validates('name')
    def validate_name(self, key, cur_name):
        if not cur_name:
            raise ValueError('Name field required.')
        return cur_name

    #must have an age between 8 and 18
    @validates('age')
    def validate_name(self, key, cur_age):
        if cur_age < 8: 
            raise ValueError('Age must be between 8 and 18.') 
        elif  cur_age > 18:
            raise ValueError('Age must be between 8 and 18.')
        return cur_age
    




    
class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    #attributes
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #foreign keys
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    #relationships
    activity = db.relationship('Activity', back_populates= 'signups_of_cur_activity')
    camper = db.relationship('Camper', back_populates = 'signups_of_cur_camper')


    #serializer_rules
    serialize_rules = ('-activity.signups_of_cur_activity', '-camper.signups_of_cur_camper')


    def __repr__(self):
        return f'<Signup {self.id}>'


    #VALIDATIONS
    #must have a time between 0 and 23 (referring to the hour of day for the activity)
    @validates('time')
    def validate_name(self, key, cur_time):
        #time_in = db.session.query(Signup.time).all()
        #for cur_time in time_in:
            if cur_time < 0: 
                raise ValueError("Signup time must be between 0 and 23")
            elif cur_time > 23:
                raise ValueError("Signup time must be between 0 and 23")
            return cur_time


# add any models you may need. 