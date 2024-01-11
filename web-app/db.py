"""this is the module that handles database interactions"""
"""import pymongo"""
from pymongo.mongo_client import MongoClient
import json 
from bson import ObjectId
from passlib.hash import bcrypt_sha256
from datetime import datetime

#docker >>
connection_string= "mongodb://db:27017"
#local client >>
#connection_string = "mongodb://localhost:27017/voiceqhub"
client = MongoClient(connection_string)
db = client["voiceqhub"]
users = db["users"]
ps = db["questionSets"]
def load_starter_data():
    """load starter data from local file"""
    #currently not used
    with open('users.json') as users_file:
        users_data = json.load(users_file)

    with open('question_sets.json') as question_sets_file:
        question_sets_data = json.load(question_sets_file)
    users.insert_many(users_data['users'])
    ps.insert_many(question_sets_data['questionSets'])

def find_ps_with_user(user):
    """search for a problem set associated with the specified user"""
    return list(ps.find({'user':user}))

def find_saved_ps(user):
    """search for all saved problem set associated with the specified user"""
    curr_user = users.find_one({'username':user})
    saved_ps = curr_user['saved']
    saved_ps_list = []
    for qid in saved_ps:
        problem_set = ps.find_one({'qid':qid})
        if (problem_set):
            saved_ps_list.append(problem_set)
    return saved_ps_list

def delete_qs(qid):
    """delete a question set with the specified id"""
    ps.delete_one({'qid':qid})
    return 

def find_ps_with_id(id):
    """find a question set with the specified id"""
    return ps.find_one({"qid": id})

def get_most_recent_ps():
    """get all question sets"""
    return list(ps.find({}))

def find_user(user):
    """find a registered user from the database"""
    return list(users.find({'user':user}))

def save_ps(username, qid):
    """save a problem set into the database"""
    user_document = users.find_one({'username': username})

    if user_document:
        # Update the 'saved' field by adding qid to the list
        users.update_one(
            {'_id': ObjectId(user_document['_id'])},
            {'$addToSet': {'saved': qid}}
        )
        print(f'Question with ID {qid} added to the "saved" list for user {username}')
    else:
        print(f'User with username {username} not found')


def check_user_and_pin(id, password):
    """verify login credentials with data in the database"""
    this_user = users.find_one({'username':id})
    if (this_user and bcrypt_sha256.verify(password,this_user['password'])):
        return True 
    else:
        return False 
    
def upload_problem_set(new):
    """upload a new problem set"""
    try:
        ps.insert_one(new)
    except(Exception):
        print("error insert to db",Exception)
    return 

def add_new_user(username, password):
    """add a new user to the database"""
    new_user = {
        'username':username,
        'password':password,
        'saved': [],
    }
    users.insert_one(new_user)
    return 

def load_sample_data():
    """load some example documents to upon server starting"""
    new_sample_user = {
        'username': 'admin@123.com',
        'password': bcrypt_sha256.hash('123'),
        'saved': ['123123'],
    }   
    new_question_set ={
        'user': 'admin@123.com',
        'name': 'sample_ps_1',
        'description': 'this is an example problem set. You can also add your own.',
        'shared': True, 
        'time': datetime.now(),
        'qid': '123123',
        'questions': [
            {
                'question': 'Please say hello',
                'answer': 'hello',
            },
            {
                'question': 'what is',
                'answer': 'what',
            }
        ],
    }
    users.insert_one(new_sample_user)
    ps.insert_one(new_question_set)

# clear saved data upon restarting. comment off if dont need 
users.delete_many({})
ps.delete_many({})
load_sample_data()
