#!/usr/bin/env python3

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}")

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Activity, Camper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

#GET /campers
class Campers(Resource):
    def get(self):
        #1. query
        campers = Camper.query.all()
        #2. dict
        campers_dict = [c.to_dict() for c in campers]
        #3. res
        res = make_response(
            campers_dict,
            200
        )
        return res

    # #POST /campers
    # def post(self):
    #     #1. set data as JSON
    #     data = request.get_json()
    #     #2. create an instance
    #     new_camper = Camper(
    #         name=data.get('camper'),
    #         age=data.get('age')
    #     )
    #     #exceptions
    #     if not new_camper:
    #         abort(404, 'Validation error')
    #     #3. add/commit
    #     db.session.add(new_camper)
    #     db.session.commit()
    #     #4. dictionary
    #     new_camper_dict = new_camper.to_dict()
    #     #5. res
    #     res = make_response(
    #         new_camper_dict,
    #         201
    #     )
    #     return res
    

#param1= name of resource class
#param2= route
api.add_resource(Campers, '/campers')


#GET /campers/int:id
class OneCamper(Resource):
    def get(self, id):
        #1. query
        camper = Camper.query.filter_by(id = id).first()
        #exception
        if not camper:
            abort('Camper not found', 404)
        #2. dict
        camper_dict = camper.to_dict()
        #3. res
        res = make_response(
            camper_dict,
            200
        )
        return res
api.add_resource(OneCamper, '/campers/<int:id>')



#GET /activities
class Activities(Resource):
    def get(self):
        #1. query
        activities = Activity.query.all()
        #2. dict
        activities_dict = [a.to_dict() for a in activities] 
        #3. res
        res = make_response(
            activities_dict,
            200
        )
        return res

api.add_resource(Activities, '/activities')



# #DELETE /activities/int:id
# class OneActivity(Resource):
#     def get(self, id):
#         #1. query
#         activity = Activity.query.filter_by(id = id).first()
#         #2. dict
#         activity_dict = [activity.to_dict()] 
#         #3. res
#         res = make_response(
#             activity_dict,
#             200
#         )
#         return res
# #DELETE /activities/int:id
#     def delete(self, id):
#         #1. get activity by id
#         activity = Activity.query.filter_by(id = id).first()
#         #2. delete/commit
#         db.session.delete(activity)
#         db.session.commit()
#         #3. return empty response
#         return make_response({}, 204)

# api.add_resource(Activity, '/activities/<int:id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)
