import json
import csv
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash_package import app

from dash.dependencies import Input, Output, State

import surprise
from surprise import dump

preds, model = dump.load('finalmodel')

colors = {
    'background': '#FFFFFF',
    'text': '#C41200'
}

with open('dash_package/dashdata.json') as f:
    dash_data_dict = json.load(f)

# full, restaurant, model
# rating_count, reviewsperbusiness, reviewsperuser

categories = list(dash_data_dict.keys())

with open('finalbusinessesindexed.json') as f:
    businesses = json.load(f)

with open('finaldata.csv', 'r') as f:
    reader = csv.reader(f)
    reviews = list(reader)

def find(f, seq):
    for item in seq:
        if f(item):
            return item

def get_info(iid):
    return find(lambda b: iid == b['id'], businesses)

def get_reviewed_restaurants(uid, desc=True):
    userreviews = list(filter(lambda r: r[0] == str(uid), reviews))
    ratings = [r[2] for r in userreviews]
    restaurants = list(map(lambda r: get_info(int(r[1])), userreviews))
    names = [r['name'] for r in restaurants]
    if desc==True:
        return sorted(list(zip(names, ratings)), reverse=True, key=lambda x: x[1])
    return sorted(list(zip(names, ratings)), key=lambda x: x[1])

def get_n_preds(uid, n):
    ratings = []
    for i in range(1, 73101):
        pred = model.predict(str(uid), str(i))
        ratings.append((int(pred.iid), pred.est))
    ratingsdesc = sorted(ratings, reverse=True, key=lambda x: x[1])[:n]
    namedratings = [(get_info(r[0])['name'], r[1], get_info(r[0])['latitude'], get_info(r[0])['longitude']) for r in ratingsdesc]
    return namedratings



app.layout = html.Div(style={'backgroundColor': colors['background'], 'font-family': 'verdana'}, children=[

    html.H1('Restaurant Recommender!', style={'textAlign': 'center', 'color': colors['text']}),

    html.H3("Slide for Users' Reviews + Recommendations", style={'textAlign': 'center', 'color': colors['text']}),

    html.Div([
				dcc.Slider(
					id='userid-slider',
					min=1,
					max=81415,
					value=1,
                    step=100,
                    marks={1: '1', 10000: '10000', 20000: '20000', 30000: '30000',
                    40000: '40000', 50000: '50000', 60000: '60000', 70000: '70000',
                    81415: '81415'}

				),
			], style={'width':1000, 'margin':40}),

    html.P('User ID Selected: {0}'.format(1),
			id = 'userid-selected',
			style = {'fontWeight':10}
		),




    html.H1('Yelp Open Dataset: Exploratory Data Analysis', style={'textAlign': 'center', 'color': colors['text'], 'padding':10}),

    html.H4('Looking into the Raw Data', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.H3('1. Distribution of Star Ratings', style={'textAlign': 'center', 'color': colors['text']}),

    html.Div([
        dcc.Dropdown(
            id='star-ratings-distribution',
            options=list(map(lambda c: {'label': c.capitalize(), 'value': c}, categories)),
            value="full"
        ),
        html.Div(id='output-stars')
    ]),

    html.H3('2. Distribution of Number of Reviews per Business', style={'textAlign': 'center', 'color': colors['text']}),

    html.Div([
        dcc.Dropdown(
            id='business-reviews-distribution',
            options=list(map(lambda c: {'label': c.capitalize(), 'value': c}, categories)),
            value="full"
        ),

        html.Div(id='output-rpb')
    ]),

    html.H3('3. Distribution of Number of Reviews per User', style={'textAlign': 'center', 'color': colors['text']}),

    html.Div([
        dcc.Dropdown(
            id='user-reviews-distribution',
            options=list(map(lambda c: {'label': c.capitalize(), 'value': c}, categories)),
            value="full"
        ),

        html.Div(id='output-rpu')
    ])



    ])

@app.callback(
	Output('userid-selected', 'children'),
	[Input('userid-slider','value')])
def update_userid(value):
    reviews = get_reviewed_restaurants(value)
    n = len(reviews)
    recs = get_n_preds(value, n)
    htmls = [html.H6(reviews[i][0]+': '+reviews[i][1]) for i in range(n)]
    urls = ['http://www.google.com/maps/place/'+str(recs[i][2])+','+str(recs[i][3]) for i in range(n)]
    preds = [html.H6([recs[i][0]+': '+str(round(recs[i][1],2))+' ', html.A('(map)', href=urls[i])]) for i in range(n)]
    return html.Div(style={'textAlign': 'center','color': colors['text']}, children=[
    html.Div([
        html.Div(children=[
            html.H4("User #{0}'s Reviews".format(value))]+htmls, className="six columns"),

        html.Div(children=[
            html.H4('Recommendations for User #{0}'.format(value))]+preds, className="six columns")
            ], className="row")
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



app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
