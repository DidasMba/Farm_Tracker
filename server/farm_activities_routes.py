from flask import Blueprint, request, jsonify
from app.models import FarmActivity
from app import db

farm_activities_routes = Blueprint('farm_activities', __name__)

@farm_activities_routes.route('/farm_activities', methods=['POST'])
def record_farm_activity():
    data = request.json

    # Validate request data
    required_fields = ['activity_type', 'date_time', 'location']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    # Specific validation and processing based on activity type
    activity_type = data['activity_type']
    if activity_type == 'planting':
        required_fields += ['crop_type']
    elif activity_type == 'harvesting':
        required_fields += ['crop_type', 'yield']
    elif activity_type == 'pesticide_application':
        required_fields += ['chemical', 'amount']

    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    # Create new farm activity object
    new_activity = FarmActivity(
        activity_type=activity_type,
        date_time=data['date_time'],
        location=data['location'],
        crop_type=data.get('crop_type'),
        yield=data.get('yield'),
        chemical=data.get('chemical'),
        amount=data.get('amount'),
        additional_info=data.get('additional_info')
    )

    # Add farm activity to database
    db.session.add(new_activity)
    db.session.commit()

    return jsonify({'message': 'Farm activity recorded successfully', 'activity': new_activity.to_dict()}), 201
