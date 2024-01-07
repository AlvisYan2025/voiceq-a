"""make a flask based app"""
from flask import Flask, jsonify, request, make_response
import speechToText

app = Flask(__name__)


@app.route("/transcript", methods=["GET"])
def recognize_and_save(my_id=1):
    """fetch the transcript from the database"""
    my_id = request.args.get("Id")
    transcript = speechToText.get_transcript()
    response = make_response(jsonify({"transcript": transcript}))
    return response


@app.route("/", methods=["GET"])
def test():
    """for testing purpose, this will display a message when a connection is successful"""
    response = make_response(jsonify({"message": "connection established"}))
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
