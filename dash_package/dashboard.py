import json
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash_package import app

from dash.dependencies import Input, Output, State

colors = {
    'background': '#FFFFFF',
    'text': '#C41200'
}

with open('dash_package/dashdata.json') as f:
    dash_data_dict = json.load(f)

categories = list(dash_data_dict.keys())

value_range = [0, 8500]

# full, restaurant, model
# rating_count, reviewsperbusiness, reviewsperuser

app.layout = html.Div(style={'backgroundColor': colors['background'], 'font-family': 'verdana'}, children=[

    html.H1('Yelp Open Dataset: Exploratory Data Analysis', style={'textAlign': 'center', 'color': colors['text']}),

    html.H3('Looking into the Raw Data', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.H2('1. Distribution of Star Ratings', style={'textAlign': 'center', 'color': colors['text']}),

    html.Div([
        dcc.Dropdown(
            id='star-ratings-distribution',
            options=list(map(lambda c: {'label': c.capitalize(), 'value': c}, categories)),
            value="full"
        ),
        html.Div(id='output-stars')
    ]),

    html.H2('2. Distribution of Number of Reviews per Business', style={'textAlign': 'center', 'color': colors['text']}),

    html.Div([
        dcc.Dropdown(
            id='business-reviews-distribution',
            options=list(map(lambda c: {'label': c.capitalize(), 'value': c}, categories)),
            value="full"
        ),

        html.Div(id='output-rpb')
    ]),

    html.H2('3. Distribution of Number of Reviews per User', style={'textAlign': 'center', 'color': colors['text']}),

    html.Div([
        dcc.Dropdown(
            id='user-reviews-distribution',
            options=list(map(lambda c: {'label': c.capitalize(), 'value': c}, categories)),
            value="full"
        ),

        html.Div(id='output-rpu')
    ]),

    ])



@app.callback(Output('output-stars', 'children'),
              [Input('star-ratings-distribution', 'value')])
def show_stars(value):
    stuff = dict(sorted(dash_data_dict[value]['rating_count'].items()))
    x = [float(k) for k in stuff.keys()]
    y = list(stuff.values())
    return html.Div([dcc.Graph(
        id='stars',
        figure={
            'data': [{'x': x, 'y': y, 'type': 'bar', 'marker': {'color': '#C41200'}}],
            'layout': {
                'title': 'Distribution of Star Ratings: ' + str(value).capitalize(),
                'margin': {'l': 30,'r': 30,'b': 30,'t': 30},
                'legend': {'x': 1, 'y': 1}
            }})])

@app.callback(Output('output-rpb', 'children'),
              [Input('business-reviews-distribution', 'value')])
def show_reviews_businesses(value):
    stuff = dash_data_dict[value]['reviewsperbusiness']
    return html.Div([dcc.Graph(
        id='businesses',
        figure={
            'data': [{'x': stuff, 'type': 'histogram', 'marker': {'color': '#C41200'}}],
            'layout': {
                'title': 'Distribution of Reviews Per Business: ' + str(value).capitalize(),
                'margin': {'l': 30,'r': 30,'b': 30,'t': 30},
                'legend': {'x': 1, 'y': 1}
            }})])

@app.callback(Output('output-rpu', 'children'),
              [Input('user-reviews-distribution', 'value')])
def show_reviews_businesses(value):
    stuff = dash_data_dict[value]['reviewsperuser']
    return html.Div([dcc.Graph(
        id='users',
        figure={
            'data': [{'x': stuff, 'type': 'histogram', 'marker': {'color': '#C41200'}}],
            'layout': {
                'title': 'Distribution of Reviews Per User: ' + str(value).capitalize(),
                'margin': {'l': 30,'r': 30,'b': 30,'t': 30},
                'legend': {'x': 1, 'y': 1}
            }})])
