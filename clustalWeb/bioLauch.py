#from flask import render_template, url_for, flash, redirect, request, session
from flask_script import Manager
from flask_cors import CORS
from app import create_app

app=create_app()
manager=Manager(app)

if __name__ == '__main__':
    CORS(app)
    app.run(debug=True)
    # manager.run()
