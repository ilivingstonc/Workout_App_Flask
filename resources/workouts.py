#resources folder is like controllers
import models
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict


# first argument is blueprints name
# second argument is it's import_name
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1, url prefix is like app.use('/fruits')
workout = Blueprint('workouts', 'workout')
#blueprint is liek the router in express, it records operations
#attach restful CRUD routes to workout blueprint

# RESTFUL ROUTES
# INDEX ROUTE
# routes default to GET
@workout.route('/', methods=['GET'])
def get_all_workouts():
    print('Current User:',  current_user)
    try:
        current_user_id = current_user.id
    except:
        return jsonify(data={}, status={"code": 401, "message": "Can't get resources"})
    workouts = [model_to_dict(workout) for workout in models.Workout.select().where(
        models.Workout.user == current_user_id
    )]

    return jsonify(data=workouts, status={'code': 200, 'message': 'Success'})

@workout.route('/<workout_id>/', methods=['GET'])
def get_workouts(workout_id):
    try:
        # Try to find workout with a certain id
        workout = model_to_dict(models.Workout.get(id=workout_id, max_depth=0))
        return jsonify(workout)
    except models.DoesNotExist:
        # If the id does not match an id of a workout in the database return 404 error
        return jsonify(data={}, status={'code': 404, 'message': 'Workout not found'})

# @login_required <- look this up to save writing some code https://flask-login.readthedocs.io/en/latest/#flask_login.login_required
@workout.route('/', methods=['POST'])
def create_workout():

    payload = request.get_json()
    print(payload, 'payload')
    if not current_user.is_authenticated: 
        # Check if user is authenticated and allowed to create a new workout - could be replaced with
        # @login_required decorator
        print(current_user)
        return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to create a workout'})
    payload['user'] = current_user.id
    created_workout = models.Workout.create(**payload)
    create_workout_dict = model_to_dict(created_workout)
    return jsonify(status={'code': 201, 'msg': 'success'}, data=create_workout_dict)

# delete route
@workout.route('/<id>/', methods=["DELETE"])
def delete_workout(id):
    
    query=models.Workout.delete().where(models.Workout.id == id)
    if current_user.is_authenticated:
        query.execute()
    # workout_to_delete = models.Workout.get(id=id)

    # if not current_user.is_authenticated: # Checks if user is logged in
    #     return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to create a workout'})
    
    # # Delete the workout and send success response back to user
    # workout_to_delete.delete()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

# Update workout route
@workout.route('/<id>/', methods=['PUT'])
def update_workout(id):
    payload = request.get_json()

    # Get the workout we are trying to update. Could put in try -> except because
    # if we try to get an id that doesn't exist a 500 error will occur. Would 
    # send back a 404 error because the 'workout' resource wasn't found.
    workout_to_update = models.Workout.get(id=id)

    if not current_user.is_authenticated: # Checks if user is logged in
        return jsonify(data={}, status={'code': 401, 'message': 'You must be logged in to edit a workout'})
    if workout_to_update.user.id is not current_user.id:
        return jsonify(data={}, status={'code': 401, 'message': 'You may only edit your workout'})
    # update form
    workout_to_update.update(
        date=payload['date'],
        title=payload['title'],
        activity=payload['activity'],
        intensity=payload['intensity'],
        duration=payload['duration'],
        description=payload['description'],
        tss=payload['tss']
    ).where(models.Workout.id==id).execute()

    # Get a dictionary of the updated workout to send back to the client.
    # Use max_depth=0 because want just the owner's id and not entire
    # owner object sent back to the client. 
    update_workout_dict = model_to_dict(workout_to_update, max_depth=0)
    return jsonify(status={'code': 200, 'msg': 'success'}, data=update_workout_dict)





