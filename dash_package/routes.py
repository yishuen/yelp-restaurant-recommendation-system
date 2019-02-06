from flask import render_template, jsonify, json

from dash_package.dashboard import app

@app.server.route('/go-to-dashboard')
def dashboard():
    return app.index()
