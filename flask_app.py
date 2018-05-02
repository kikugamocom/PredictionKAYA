import pyrebase
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
import json
import arrow
import tensorflow as tf
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt
from flask_cors import CORS

from predict_bin import Bin_predict


bin_predictor = Bin_predict()
auth = HTTPBasicAuth()

app = Flask(__name__)

cors = CORS(app, resources={r"/predict_bin/*": {"origins": "*"}})

 


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    #Secrets
    config = {
    
    }

    #Secrets
    email = ""
    password = ''


    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    db = firebase.database()

    user = auth.sign_in_with_email_and_password(email, password)
    bin_info = db.child('kaya/bin').get(user['idToken'])
    bin_info = bin_info.val()
    print(bin_info.keys())
    #return jsonify({'tasks': [make_public_task(task) for task in tasks]})
    #return bin_info.keys()
   
    return jsonify({'task': bin_info})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

#TODO
# bin_pred = Bin_predict(....)

@app.route('/predict_bin/<sensor_id>/<target_time>', methods=['GET'])
def predict_bin(sensor_id, target_time):    
    predicted_lv = bin_predictor.predict_lv(sensor_id, target_time)
    if predicted_lv != -1:
        return jsonify({'predicted_lv': predicted_lv})
    elif predicted_lv == -2:
        return jsonify({'predicted_lv': 'model no learn'})
    else:
        return jsonify({'predicted_lv': 'fail'})

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@auth.get_password
def get_password(username):
    if username == 'parnza':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)





if __name__ == '__main__':
    app.run(debug=True)