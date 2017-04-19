from flask import Flask, send_from_directory
from flask import render_template
from flask_restful import Resource, Api
from rest.login import Login
from dao.models import MarshallableModel
import configparser
from dao.base import init_db
import os

BASE_URL = os.path.abspath(os.path.dirname(__file__))
CLIENT_APP_FOLDER = os.path.join(BASE_URL, "templates")

app = Flask(__name__)
api = Api(app)
api.add_resource(Login, '/login')



@app.route('/')
def hello_world():
    return render_template('index.html');

@app.route('/<path:filename>')
def client_app_folder(filename):
    return send_from_directory(CLIENT_APP_FOLDER, filename)


if __name__ == '__main__':
    init_db()
    MarshallableModel.init_marshallers()
    app.run()

