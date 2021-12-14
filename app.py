# ======= App Imports =========
from flask import Flask, request, jsonify
from models import db, User, Post, Category
from flask_migrate import Migrate
import uuid
import json
import jsonpickle
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, create_refresh_token, JWTManager, jwt_required

# ======= END App Imports =========


app = Flask(__name__)
app.config.from_pyfile("config.py", silent=True)
jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

with app.app_context():
    db.create_all()


def check_incoming_data(package):
    try:
        if package:
            incoming_data = package.get_json(force=True)
        else:
            incoming_data = package.data.decode(encoding="utf-8")
            incoming_data = json.dumps(incoming_data)

        return incoming_data
    except Exception as e:
        return False


def check_incoming_user(somedata):
    try:
        incoming_data = check_incoming_data(somedata)

        if not incoming_data:
            raise ValueError("Invalid data")

        if "username" not in incoming_data:
            raise ValueError("Missing username")

        if "password" not in incoming_data:
            raise ValueError("Missing password")

        return incoming_data
    except Exception as e:
        return False


# ======= Resource Classes =========
class HelloWorld(Resource):
    def get(self):
        return {'Test Check': 'tis working'}


class Register(Resource):
    def post(self):
        try:
            if request:
                incoming_data = request.get_json()
                # print(type(incoming_data))
            else:
                incoming_data = request.data.decode(encoding="utf-8")
                incoming_data = json.dumps(incoming_data)
                print(type(incoming_data))

            if "password" not in incoming_data:
                raise ValueError("Missing password")

            new_user = User(**incoming_data)

            hashed_password = User.create_password_hash(incoming_data["password"])

            if not hashed_password:
                raise ValueError("Password error")
            new_user.password = hashed_password

            token = f"{uuid.uuid4()}"
            new_user.token = token

            db.session.add(new_user)
            db.session.commit()

            return {"email": new_user.email, "token": token}, 201
        except Exception as e:
            print(f"{e}")
            return incoming_data, 400


# class LoginUser(Resource):
#     def post(self):
#         try:
#             if request.get_json():
#                 incoming_data = request.get_json()
#             else:
#                 incoming_data = request.data.decode(encoding="utf-8")
#                 incoming_data = json.dumps(incoming_data)
#
#             users = db.session.query(User).all()
#             current_users = []
#             for user in users:
#                 current_users.append([user.user_name, user.email, user.password, user.is_admin])
#         except:
#             print("hello")


class LoginUser(Resource):
    def post(self):

        if request.get_json():
            incoming_data = request.get_json()
            # print(type(incoming_data))
        else:
            incoming_data = request.data.decode(encoding="utf-8")
            incoming_data = json.dumps(incoming_data)

        if not incoming_data:
            raise ValueError("Invalid User Data")

        user = db.session.query(User).filter_by(user_name=incoming_data['user_name']).one_or_none()

        if not user:
            raise ValueError("Can't find the User in the Database")

        print(type(incoming_data['password']))

        hashed_password = User.create_password_hash(incoming_data['password'])

        # if not user.password_is_verified(incoming_data['password']):
        if not user.password_is_verified(hashed_password):
            raise ValueError("Invalid Password")

        # access_token = create_access_token(
        #     identity=user,
        #     additional_claims={"is_admin": user.is_admin}
        # )
        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)

        return {"refresh": refresh_token, "access": access_token}, 200


# class UserMe(Resource):
#     @jwt_required()
#     def get(self):
#         try:
#             return current_user.as_dict_short, 200
#         except Exception as e:
#             return {"error:" f"{e}"}, 400


class MakePost(Resource):
    def post(self):
        try:
            auth_token = request.headers.get("Authorization", None)
            if not auth_token:
                raise ValueError("Missing or invalid Authorization header")
            if auth_token.startswith("Bearer "):
                auth_token = auth_token[7:]
            if request.get_json():
                incoming_data = request.get_json()
            else:
                incoming_data = request.data.decode(encoding="utf-8")
                incoming_data = json.dumps(incoming_data)
            auth_user = db.session.query(User).filter(User.token == auth_token)
            if not auth_user[0]:
                raise ValueError(f"Invalid or missing User. Token looks incorrect: {auth_token}.")
            post_dict = {
                "owner_id": auth_user[0].id,
                "category_id": incoming_data["category_id"],
                "title": incoming_data["title"],
                "content": incoming_data["content"]
            }
            new_post = Post(**post_dict)
            db.session.add(new_post)
            db.session.commit()

            return incoming_data, 201
        except Exception as e:
            print(f"{e}")
            return incoming_data, 400


class MakeCategory(Resource):
    def post(self):

        if request.get_json():
            incoming_data = request.get_json()
        else:
            incoming_data = request.data.decode(encoding="utf-8")
            incoming_data = json.dumps(incoming_data)

        post_dict = {

            "name": incoming_data["name"],
            "hashtag": incoming_data["hashtag"],
            "description": incoming_data["description"]
        }
        new_post = Post(**post_dict)
        db.session.add(new_post)
        db.session.commit()


class ListPosts(Resource):
    def get(self):
        posts = db.session.query(Post).all()
        returning_json = {"posts": []}
        for post in posts:
            returning_json["posts"].append(
                {
                    "id": post.id,
                    "owner": f"{post.owner}",
                    "category": f"{post.category}",
                    "title": post.title,
                    "content": post.content,
                    "created": f"{post.created}",
                    "updated": f"{post.updated}"
                }
            )
        return returning_json


class ListCategories(Resource):
    def get(self):
        categories = db.session.query(Category).all()
        returning_json = {"categories": []}
        for category in categories:
            returning_json["categories"].append(
                {
                    "id": category.id,
                    "name": f"{category.name}",
                    "hashtag": f"{category.hashtag}",
                    "description": category.description,
                    "created": f"{category.created}",
                    "updated": f"{category.updated}"
                }
            )
        return returning_json


class ListUsers(Resource):
    def get(self):
        users = db.session.query(User).all()
        returning_json = {"users": []}
        for user in users:
            returning_json["users"].append(
                {
                    "id": user.id,
                    "name": f"{user.name}",
                    "email": f"{user.email}",
                    "token": user.token,
                    "created": f"{user.created}",
                    "updated": f"{user.updated}"
                }
            )
        return returning_json

class UserList(Resource):
    def get(self):
        users = User.as_dict
        return users

class ListUsersFullName(Resource):
    def get(self):
        users = db.session.query(User).all()
        returning_json = {"users": []}
        for user in users:
            returning_json["users"].append(
                {
                    "name": f"{user.fullname}"
                }
            )
        return returning_json


# ======= END Resource Classes =========


# ======= Resource Endpoints =========
api.add_resource(HelloWorld, "/")
api.add_resource(ListUsers, "/list-users/")
api.add_resource(ListUsersFullName, "/list-users-full-name/")
api.add_resource(UserList, "/user-list/")
api.add_resource(ListPosts, "/list-posts/")
api.add_resource(ListCategories, "/list-categories/")
api.add_resource(MakeCategory, "/make-category/")
api.add_resource(MakePost, "/create-post/")
api.add_resource(Register, "/register/")
api.add_resource(LoginUser, "/login/")
# api.add_resource(UserMe, "/userme/")


# ======= END Resource Endpoints =========


# run flask app
if __name__ == "__main__":
    app.run(debug=True)
