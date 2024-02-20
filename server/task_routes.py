from flask import Blueprint, request, jsonify
from app.models import Task
from app import db

task_routes = Blueprint('tasks', __name__)

@task_routes.route('/tasks', methods=['POST'])
def add_task():
    data = request.json

    # Validate request data
    if not data.get('description') or not data.get('type'):
        return jsonify({'error': 'Description and type are required'}), 400

    # Create new task object
    new_task = Task(
        description=data['description'],
        type=data['type'],
        assigned_worker=data.get('assigned_worker'),
        deadline=data.get('deadline')
    )

    # Add task to database
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task added successfully', 'task': new_task.to_dict()}), 201
