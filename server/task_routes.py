# from flask import Blueprint, request, jsonify
# from app.models import Task, Worker  # Import Worker model
# from app import db

# task_routes = Blueprint('tasks', __name__)

# @task_routes.route('/tasks', methods=['POST'])
# def add_task():
#     data = request.json

#     # Validate request data
#     if not data.get('description') or not data.get('type'):
#         return jsonify({'error': 'Description and type are required'}), 400

#     # Create new task object
#     new_task = Task(
#         description=data['description'],
#         type=data['type'],
#         assigned_worker=data.get('assigned_worker'),  # Make sure this matches your Task model
#         deadline=data.get('deadline')
#     )

#     # Add task to database
#     db.session.add(new_task)
#     db.session.commit()

#     return jsonify({'message': 'Task added successfully', 'task': new_task.to_dict()}), 201

# @task_routes.route('/tasks/<int:task_id>/assign', methods=['PUT'])
# def assign_task(task_id):
#     data = request.json

#     # Validate request data
#     if not data.get('worker_id'):
#         return jsonify({'error': 'Worker ID is required'}), 400

#     # Retrieve task and worker from database
#     task = Task.query.get(task_id)
#     worker = Worker.query.get(data['worker_id'])
#     if not task or not worker:
#         return jsonify({'error': 'Task or Worker not found'}), 404

#     # Assign task to worker
#     task.assigned_worker_id = worker.id  # Make sure this matches your Task model

#     # Commit changes to database
#     db.session.commit()

#     return jsonify({'message': 'Task assigned successfully', 'task': task.to_dict()}), 200


