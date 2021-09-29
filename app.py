from flask import Flask, render_template, request, redirect
import json
import plotly
import plotly.graph_objs as go
from src.config import bots, coins
from src.db import records_query
from dateutil import parser
app = Flask(__name__)
import datetime
'''    {% autoescape false %}
    {{descr}}
    {% endautoescape %}'''

# https://cdn2.scratch.mit.edu/get_image/gallery/27020427_170x100.png FLYING TACO
# https://media0.giphy.com/media/6SMPIQVz4NHk6vLU29/giphy.gif?cid=6c09b952a2410c9be8f024561ecaca53491ccbe4dc247fe7&rid=giphy.gif&ct=s JJK DANCE


@app.route('/', methods=['GET', 'POST'])
def index():
    s_date = datetime.datetime.today()
    e_date = datetime.datetime.today() + datetime.timedelta(days=1)
    return render_template('content.html', bots=bots, coins=list(coins.keys()), task='index', dates=[s_date.strftime("%Y-%m-%d"), e_date.strftime("%Y-%m-%d")])


@app.route('/graph', methods=['GET', 'POST'])
def bots_graphs():
    bname = request.form.get('bots')
    coin = request.form.get('coins')
    s_date = request.form.get('sd')
    e_date = request.form.get('ed')
    if None in [bname, coin, s_date, e_date]:
        return redirect("/", code=302)
    if s_date != '':
        s_date = parser.parse(s_date)
    if e_date != '':
        e_date = parser.parse(e_date)
    botd = list(a for a in bots if a['name'] == bname)
    if len(botd) == 0 or len(botd) > 1:
        return '<p> WTFFFFFFF </p>'
    df = records_query(s_date, e_date, coins[coin])
    binance = go.Scatter(x=df['timestamp'].tolist(), y=df['values'].tolist(), name='Binance')
    bot = go.Scatter(x=df['timestamp'].tolist(), y=list(float(a)*1.01 for a in df['values'].tolist()), name=bname)
    graph = json.dumps([binance, bot], cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('content.html', bots=bots, coins=list(coins.keys()), graph=graph, bname=bname, task='graph', dates=[request.form.get('sd'), request.form.get('ed')])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)