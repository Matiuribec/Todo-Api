"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Todos
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/todos/<int:user_param>', methods=['GET'])
def get_todos(user_param):
    todos= Todos.query.filter(Todos.user_id==user_param).all()
    user_data=todos[0].user.serialize()
    return jsonify ({
        "user":user_data,
        "todos": list(map(lambda item: item.serialize(), todos))
    }), 200 

@api.route('/todos/<int:user_param>', methods=['POST'])
def post_todos(user_param):
    label = request.json.get("label")
    done = request.json.get("done")
    newTodo = Todos(user_id=user_param, label=label, done=done) #el Todos es lo que estoy importando desde arriba, de models
    db.session.add(newTodo)#con el db session lo que hago es que lo agrego a la base de datos al newTodo  
    db.session.commit()

    return jsonify ({"resp": "todo creado con exito"}), 201

@api.route('/todos/<int:user_param>/<int:todo_index>', methods=['PUT'])
def update_todos(user_param, todo_index):
    label = request.json.get("label")
    done = request.json.get("done")
    todos= Todos.query.filter(Todos.user_id==user_param).all()
    newTodo= todos[todo_index]
    newTodo.label=label
    newTodo.done=done
    db.session.add(newTodo)
    db.session.commit()

    return jsonify ({"resp": "todo actualizado con exito"}), 200 


@api.route('/todos/<int:user_param>/<int:todo_index>', methods=['DELETE'])
def delete_todos(user_param, todo_index):
    todos= Todos.query.filter(Todos.user_id==user_param).all()
    todo_delete= todos[todo_index]
    db.session.delete(todo_delete)
    db.session.commit()

    return jsonify ({"resp": "todo eliminado con exito"}), 200