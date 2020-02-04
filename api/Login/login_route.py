from flask import Blueprint,request,jsonify
from api.User.user_model import User
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash 

login=Blueprint('login', __name__)

@login.route('/login', methods=["POST"])
def log_in():
    request_data = request.get_json()

    user=User.query.filter_by(email=request_data["email"]).first()
    if user:
        if check_password_hash(user.password,request_data["password"]):
            jwt_token=create_access_token(identity=user.email)
            return jsonify({"token":jwt_token})
    else:
        return "Invalid email or password",400