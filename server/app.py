from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_serialized = [message.to_dict() for message in messages]
        response = make_response(messages_serialized, 200)

    elif request.method == 'POST':
        data = request.get_json()
        message = Message(
            username = data['username'],
            body = data['body']
            # username = request.form.get('username'),
            # body = request.form.get('body')
        )
        # print(message.to_dict())
        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()
        print(message_dict)

        response = make_response(message_dict, 201)

    return response

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()
        response = make_response(message_dict, 200)

    if request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response = make_response(
            {"Message Deleted": True},
            200
        )

    return response



if __name__ == '__main__':
    app.run(port=5555)
