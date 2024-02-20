from flask import Blueprint, request, jsonify
from app.models import Task
from app import db

task_routes = Blueprint('tasks', __name__)

@task_routes.route('/tasks/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    data = request.json

    # Validate request data
    if not data.get('status'):
        return jsonify({'error': 'Status is required'}), 400

    # Retrieve task from database
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    # Update task status
    task.status = data['status']

    # Commit changes to database
    db.session.commit()

    return jsonify({'message': 'Task status updated successfully', 'task': task.to_dict()}), 200
