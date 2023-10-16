from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Sessions(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        user = User.query.filter_by(username=username).first()
        if user:
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {'message': 'Invalid username'}, 401

    def delete(self):
        session.pop('user_id', None)
        return {}, 204

    def get(self):
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            if user:
                return user.to_dict(), 200
        return {}, 401

api.add_resource(Sessions, '/login', '/logout', '/check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
