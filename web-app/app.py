# pylint: disable=no-member
"""Import modules"""
import os
import requests  
import fuzzywuzzy as fuzz
from passlib.hash import bcrypt_sha256
from flask import Flask, jsonify, request, render_template, make_response, session, redirect
from flask_session import Session
import uuid 
from datetime import datetime
import db


app = Flask(__name__, template_folder="templates")
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './sessions'
app.config['SESSION_KEY_PREFIX'] = 'test_'
Session(app)

# Set up the upload folder for audio files
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
current_question = None  # pylint: disable=invalid-name
correct_answer = ""  # pylint: disable=invalid-name

def get_transcript():
    """Function to get the most recent transcript from an external service"""
    target_url = "http://mlc:3000/transcript"
    response = requests.get(target_url)

    if response.status_code == 200:
        json_data = response.json()
        transcript = json_data.get("transcript", "")
        print(transcript)
        return transcript
    else:
        print("Error:", response.status_code)

def check_answer(ans1, ans2):
    """helper function to compare the input with the actual answer"""
    #currently not in use
    ratio = fuzz.ratio(ans1, ans2)
    if (ratio>=60):
        return True 
    return False 

@app.route("/")
def index():
    """display the home page"""
    if ('user_id' in session):
        return render_template("homepage.html", user=session['user_id'])
    else:
         return render_template("homepage.html")


@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    """Route for handling audio file uploads"""
    # Save the uploaded audio file and print a success message
    f = request.files["audio_data"]
    with open("uploads/audio.wav", "wb") as audio:
        f.save(audio)
    print("File uploaded successfully")

    # Get the transcript and compare it with the correct answer
    transcript = get_transcript() or "Please say again"
    transcript = str(transcript.strip())
    response = make_response(
        jsonify(
            {
                "transcript": transcript,
            }
        )
    )
    return response

@app.route("/upload", methods=['GET'])
def show_upload_screen():
    """show screen to upload new question set"""
    return render_template("addquestions.html")

@app.route("/login", methods=["GET"])
def show_login_screen():
    """show login screen"""
    message = request.args.get('message')
    if message:
        return render_template('login.html',message=message)
    if ('user_id' in session):
        return render_template("homepage.html", message = 'you are logged in')
    return render_template("login.html")

@app.route("/register", methods = ["GET"])
def show_registration_screen():
    """show screen to register new user"""
    return render_template("register.html")

@app.route("/ps", methods=["GET"])
def get_problem_set():
    """api to serve all question sets"""
    if ('user_id' in session):
        print(session['user_id'])
        problem_sets_user=db.find_ps_with_user(session['user_id'])
        for doc in problem_sets_user:
            doc['_id'] = str(doc['_id'])
        problem_sets_saved=db.find_saved_ps(session['user_id'])
        for doc in problem_sets_saved:
            doc['_id'] = str(doc['_id'])
        print(problem_sets_user, problem_sets_saved)
    else:
        problem_sets_user = None 
        problem_sets_saved = None
    problem_sets = db.get_most_recent_ps()
    for doc in problem_sets:
        doc['_id'] = str(doc['_id'])
    response = jsonify({
        "problem_sets": problem_sets,
        "user": problem_sets_user,
        "saved": problem_sets_saved,
    })
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route("/save", methods=["GET"])
def save_ps():
    """save a problem set"""
    qid = request.args.get('qid')
    if ('user_id' in session):
        db.save_ps(session['user_id'],qid)
    return redirect('/')

@app.route("/my-profile", methods=["GET"])
def show_profile_screen():
    """show user profile"""
    if ('user_id' in session):
        problem_sets_user=db.find_ps_with_user(session['user_id'])
        return render_template('my-profile.html', user=session['user_id'], ps=problem_sets_user)
    else:
        return render_template('homepage.html')

@app.route("/about", methods=["GET"])
def show_info_screen():
    """show info and instructions screen"""
    return render_template("about.html")

@app.route("/logout", methods=['GET'])
def logout():
    """logout current user"""
    if ('user_id') in session:
        session.pop('user_id', None)
    return redirect('/')

@app.route("/question", methods=['GET'])
def get_question():
    """api to serve one question set"""
    qid = request.args.get('qid')
    ps = db.find_ps_with_id(qid)
    return render_template('question.html',qid=qid, name=ps['name'], description=ps['description'],time=ps['time'],questions=ps['questions'])

@app.route("/remove", methods=["GET"])
def delete_question_set():
    """remove a question set from the database"""
    qid = request.args.get('qid')
    db.delete_qs(qid)
    return redirect('/my-profile')

@app.route('/upload', methods=['POST'])
def upload_question_set():
    """uploads a quesetion set to the database"""
    data = request.get_json()
    question_list = data.get('questions')
    name = data.get('name')
    description = data.get('description')
    print(question_list)
    new_question_list ={
        'user': None,
        'name': name,
        'description': description,
        'shared': False,
        'time': datetime.now(),
        'qid': str(uuid.uuid4()),
        'questions': [],
    }
    for question in question_list:
        print(question)
        q = question['question']
        a = question['answer']
        new_question_list["questions"].append({'question':q,"answer":a,})
    if 'user_id' in session:
        new_question_list['user']=session['user_id']
    db.upload_problem_set(new_question_list)
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    """receive credencials from the from and verify in the db. If authenticated, log the user in """
    user = request.form.get('user')
    password = request.form.get('password')
    #TODO: check in db 
    if (db.check_user_and_pin(user, password)):
        session['user_id']=user
        return redirect('/')
    else:
        return redirect('/login?message=invalid credentials')

@app.route('/register', methods=['POST'])
def register_user():
    """register new user"""
    user = request.form.get('user')
    password = request.form.get('password')
    if (db.check_user_and_pin(user, password)):
        return redirect('/login?message=user existed')
    hashed_password = bcrypt_sha256.hash(password)
    db.add_new_user(user, hashed_password)
    session['user_id']=user
    return redirect('/')

def create_app():
    """return an app object, used for testing"""
    return app


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    app.run(host="0.0.0.0", port=4000)
