from flask import Blueprint, jsonify, request
from database.__init__ import database
import app_config as config
from models.Task_model import Task
import controllers.Task_controller as Task_controller
from helpers.token_validation import validate_token

from bson import ObjectId
task=Blueprint("task",__name__)


@task.route('/Tasks/', methods=['POST'])
def Create_Task():
    try:
        token=validate_token()
    
        if token==400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401 
        if token==401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403 
  



        task_data=request.json
        if 'description'not in task_data or 'email' not in task_data:
            raise Exception('Error validating form') 
        print(task_data)


    #finds info on receiver(assignedTo)
        receiver=Task_controller.fetch_user_info(task_data.get('email'))
    #finds info on creator(createdBy)
        Creator=Task_controller.fetch_user_info(token.get('email'))
        print('creator',Creator)
        print('receiver',receiver)

        new_task=Task(
            createdByUid=Creator['id'],
            createdByName=Creator['email'],
            assignedToUid=receiver['id'],
            assignedToName=receiver['name'],
            description=task_data['description'],
            done=False,
        )
        print(new_task)
        createdTask=database.database[config.CONST_TASK_COLLECTION].insert_one(new_task.__dict__)
    
        return jsonify({'message': 'task reussit','task_id': str(createdTask.inserted_id)})
    except:
        return jsonify({'error': 'Something went wrong!'}), 500

@task.route('/Tasks/createdby/', methods=['GET'])
def TaskSendToUser():
    try:
        token=validate_token()
        if token==400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401 
        if token==401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403 
   



        result, code=Task_controller.fetch_tasks(token,'createdByUid')
    
        return result, code
    except:
        return jsonify({'error': 'Something went wrong!'}), 500


@task.route('/Tasks/assignedto/', methods=['GET'])
def TaskAssignToUser():
    try:
        token=validate_token()
        if token==400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401 
        if token==401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403 
    
        result, code=Task_controller.fetch_tasks(token,'assignedToUid')
        
        return result, code
    except:
        return jsonify({'error': 'Something went wrong!'}), 500



@task.route('/Tasks/<taskUid>', methods=['PATCH'])
def UpdateTask(taskUid):
    try:
        taskUid = ObjectId(taskUid)
        token=validate_token()
        if token==400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401 
        if token==401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403 
       


        task= database.database[config.CONST_TASK_COLLECTION].find_one({'createdByUid': ObjectId(token['id']),'_id':taskUid})
        if task is None:
            raise Exception('Task not found within task assigned to user               ')
        
        
        
        
        database.database[config.CONST_TASK_COLLECTION].update_one({'_id': ObjectId(task['_id'])}, {'$set': {'done': True}})
            
        return jsonify({"taskUid": f"{task['_id']}"}),200

        
        
    except:
        return jsonify({'error': 'Something went wrong!'}), 500


@task.route('/v1/Tasks/<taskUid>', methods=['DELETE'])
def delete_task(taskUid):
    try:
        taskUid = ObjectId(taskUid)
        token=validate_token()
        if token==400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401 
        if token==401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403 
    

        task= database.database[config.CONST_TASK_COLLECTION].find_one({'createdByUid': ObjectId(token['id']),'_id':taskUid})
        print(task)
        if task is None:
            raise Exception('Users can only delete when task is created by them.') 
    
   

    
        database.database[config.CONST_TASK_COLLECTION].delete_one({'_id': ObjectId(task['_id'])})
        if task.deleted_count>0:
            return jsonify({'tasksAffected': task.deleted_count}), 200 
    except:
        return jsonify({'error': 'Something went wrong!'}), 500
   