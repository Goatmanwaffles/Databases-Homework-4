#IMPORTS
from flask import Flask, render_template, request, jsonify
import json
import config
import pymysql

#Configuration for Database
db = config.dbserver

#App Configuration
app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template('index.html')
