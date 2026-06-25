from flask import Flask, make_response, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, User, UserSchema

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

# Define routes

class Login(Resource):

    def post(self):
        user = User.query.filter(User.username == request.get_json()["username"]).first()

        if user:
            session["user_id"] = user.id
            return UserSchema().dump(user)
        else:
            return {"message": "Invalid login"}, 401
        
class CheckSession(Resource):

    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return UserSchema().dump(user)
        else:
            return {'message': '401: Not Authorized'}, 401

class Logout(Resource):
    def delete(self):
        session["user_id"] = None

        return {"massage": "204: Not Authorized"}, 204
    

api.add_resource(Login, "/login")
api.add_resource(CheckSession, '/check_session')
api.add_resource(Logout, "/logout")

if __name__ == '__main__':
    app.run(port=5556, debug=True)