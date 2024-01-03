"""import pymongo"""
from pymongo.mongo_client import MongoClient
import json 
from bson import ObjectId


#client = MongoClient("mongodb://db:27017")
connection_string = "mongodb://localhost:27017/voiceqhub"
client = MongoClient(connection_string)
db = client["voiceqhub"]
users = db["users"]
ps = db["questionSets"]
ps.delete_many({})
def load_starter_data():
    with open('users.json') as users_file:
        users_data = json.load(users_file)

    with open('question_sets.json') as question_sets_file:
        question_sets_data = json.load(question_sets_file)
    users.insert_many(users_data['users'])
    ps.insert_many(question_sets_data['questionSets'])

def find_ps_with_user(user):
    return list(ps.find({'user':user}))

def find_saved_ps(user):
    curr_user = users.find_one({'username':user})
    saved_ps = curr_user['saved']
    saved_ps_list = []
    for pid in saved_ps:
        problem_set = ps.find_one({'pid':pid})
        if (problem_set):
            saved_ps_list.append(problem_set)
    return saved_ps_list

def find_ps_with_id(id):
    return ps.find_one({"qid": id})

def get_most_recent_ps():
    return list(ps.find({}))

def find_user(user):
    return list(users.find({'user':user}))

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
        'saved': [],
    }
    users.insert_one(new_user)
    return 

