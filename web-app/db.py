"""import pymongo"""
from pymongo.mongo_client import MongoClient
import json 
from bson import ObjectId

connection_string = "mongodb://db:27017/?directConnection=true&appName=mongosh+2.1.0"
#client = MongoClient("mongodb://db:27017")
client = MongoClient('connection_string')
print(client)
db = client["voiceqhub"]
print(db)
users = db["users"]
ps = db["questionSets"]
ps.insert_one({'test':'test'})
def load_starter_data():
    with open('users.json') as users_file:
        users_data = json.load(users_file)

    with open('question_sets.json') as question_sets_file:
        question_sets_data = json.load(question_sets_file)
    users.insert_many(users_data['users'])
    ps.insert_many(question_sets_data['questionSets'])

def find_ps_with_user(user):
    ps.find({'user':user})

def find_ps_with_id(id):
    ps.find({"__id":id})

def get_most_recent_ps():
    ps.find({})

def find_user(user):
    return users.find({'user':user})

def check_user_and_pin(id, password):
    this_user = users.find({'user':id, 'password':password})
    if (this_user):
        return True 
    else:
        return False 
    
def get_most_recent_transcript():
    """fetch the most recent transcript from the database"""
    '''try:
        documents_with_time = collection.find({"time": {"$exists": True}})
        most_recent_document = max(documents_with_time, key=lambda x: x["time"])
        return most_recent_document["transcript"]
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error: {e}")
        return None'''

def upload_problem_set(new):
    try:
        ps.insert_one(new)
    except(Exception):
        print("error insert to db",Exception)
    return 

def add_new_user(username, password):
    new_user = {
        'username':username,
        'password':password,
    }
    users.insert_one(new_user)
    return 

