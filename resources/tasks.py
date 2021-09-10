from flask import request, jsonify, Blueprint
from datetime import datetime

from database import tasks

task_bp = Blueprint('routes-tasks', __name__)


@task_bp.route('/task', methods=['POST']) 
def add_task():
    title = request.json['title']
    created_date = datetime.now().strftime("%x") # 2/22/2021
    data = (title,created_date)
    task_id = tasks.insert_task(data)

    if task_id:
        task = tasks.select_task_by_id(task_id)
        return jsonify({'task': task})
    
    return jsonify({'mesasage': 'Internal Error'})

@task_bp.route('/task', methods=['GET']) 
def get_tasks(): 
    data = tasks.select_all_tasks()

    if data: 
        return jsonify({'tasks': data}) 
    elif data: 
        return jsonify({'message':'Internal Error'})
    else:
        return jsonify({'tasks': {}})

@task_bp.route('/task', methods=['PUT']) 
def update_task():
    title = request.json['title']     
    id_arg = request.args.get('id')

    if tasks.update_task(id_arg, (title,)):
        task = tasks.select_task_by_id(id_arg)
        return jsonify(task)
    return jsonify({'message':'Internal Error'})
    
@task_bp.route('/task', methods=['DELETE']) 
def delete_task():
    id_arg = request.args.get('id')

    if tasks.delete_task(id_arg):
        return jsonify({'message':'Task Deleted'})
    return jsonify({'message':'Internal Error'})


@task_bp.route('/task/completed', methods=['PUT']) 
def completed_task():
    id_arg = request.args.get('id')
    complete_arg = request.args.get('completed')

    if tasks.complete_task(id_arg, complete_arg):
        task = tasks.select_task_by_id(id_arg)
        return jsonify({'message':'Succesfully'})
    return jsonify({'message':'Internal Error'})