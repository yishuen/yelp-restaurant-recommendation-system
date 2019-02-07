from flask import Flask
import dash

server = Flask(__name__)
# add configurations and database
server.config['DEBUG'] = True

app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')
app.config['suppress_callback_exceptions']=True

from dash_package import routes
