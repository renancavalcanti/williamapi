from database.__init__ import database
import app_config as config
import bcrypt
from datetime import datetime, timedelta
import jwt
import models.Task_model as Task
from flask import jsonify
from bson import ObjectId

def fetch_user_info(email):
    collection= database.database[config.CONST_USER_COLLECTION].find({'email':email})
    
    for users in collection:
        user= {'name':users['name'],
            'email':users['email'],
            'id':users['_id']
            }


        
    return user

def fetch_tasks(token,field):
    
    collection=database.database[config.CONST_TASK_COLLECTION].find({field: ObjectId(token['id'])})
 
    Task = []
   
    for task in collection:
        
        tasks = {
            'id':str(task['_id']),
            'assignedToUid':str(task['assignedToUid']),
            'assignedToName': task['assignedToName'],
            'description': task['description'],
            'createdByName': task['createdByName'], 
            'createdByUid': str(task['createdByUid']), 
            'done': task['done'],  
        }
        
        Task.append(tasks)
   
    return jsonify({'task':Task}), 200


