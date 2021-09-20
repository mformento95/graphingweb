from flask import Flask, render_template, request
import json
import plotly
import plotly.graph_objs as go
from src.config import bots
from src.db import last_binance

app = Flask(__name__)

'''    {% autoescape false %}
    {{descr}}
    {% endautoescape %}'''

# https://cdn2.scratch.mit.edu/get_image/gallery/27020427_170x100.png FLYING TACO
# https://media0.giphy.com/media/6SMPIQVz4NHk6vLU29/giphy.gif?cid=6c09b952a2410c9be8f024561ecaca53491ccbe4dc247fe7&rid=giphy.gif&ct=s JJK DANCE


@app.route('/', methods=['GET', 'POST'])
def index():
    graph="{{}}"
    return render_template('index.html', bots=bots, graph=graph, )


@app.route('/bots/<bname>', methods=['GET', 'POST'])
def bots_graphs(bname):
    botd = list(a for a in bots if a['name'] == bname)
    if len(botd) == 0 or len(botd) > 1:
        return '<p> WTFFFFFFF </p>'
    df = last_binance(1)
    binance = go.Scatter(x=df['timestamp'].tolist(), y=df['values'].tolist(), name='Binance')
    bot = go.Scatter(x=df['timestamp'].tolist(), y=list(float(a)*1.01 for a in df['values'].tolist()), name=bname)
    graph = json.dumps([binance, bot], cls=plotly.utils.PlotlyJSONEncoder)
    print(bots)
    return render_template('bots.html', bots=bots, graph=graph, bname=bname)


@app.route('/all', methods=['GET', 'POST'])
def all():
    bname = 'Etna'
    botd = list(a for a in bots if a['name'] == bname)
    if len(botd) == 0 or len(botd) > 1:
        return '<p> WTFFFFFFF </p>'
    df = last_binance(1)
    binance = go.Scatter(x=df['timestamp'].tolist(), y=df['values'].tolist(), name='Binance')
    bot = go.Scatter(x=df['timestamp'].tolist(), y=list(float(a)*1.01 for a in df['values'].tolist()), name=bname)
    graph = json.dumps([binance, bot], cls=plotly.utils.PlotlyJSONEncoder)
    print(bots)
    return render_template('index.html', bots=bots, graph=graph)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)