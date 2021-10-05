from flask import Flask, render_template, request, redirect
import json
import plotly
import plotly.graph_objs as go
from src.config import bots, coins
from src.db import records_query, results_query
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
    return render_template('content.html', bots=bots, coins=list(coins.keys()), task='index',
                           dates=[s_date.strftime("%Y-%m-%d"), e_date.strftime("%Y-%m-%d")])


@app.route('/binance', methods=['POST'])
def binance_graphs():
    coin = request.form.get('coins')
    s_date = request.form.get('sd')
    e_date = request.form.get('ed')
    if None in [coin, s_date, e_date]:
        return redirect("/", code=302)
    if s_date != '':
        s_date = parser.parse(s_date)
    if e_date != '':
        e_date = parser.parse(e_date)
    df = records_query(s_date, e_date, coins[coin])
    i_coins = list(coins.keys())
    i_coins.remove(coin)
    i_coins.insert(0, coin)
    binance = go.Scatter(x=df['timestamp'].tolist(), y=df['values'].tolist(), name='Binance')
    # bot = go.Scatter(x=df['timestamp'].tolist(), y=list(float(a)*1.01 for a in df['values'].tolist()), name=bname)
    graph = json.dumps([binance], cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('content.html', coins=i_coins, graph=graph, task='binance',
                           dates=[request.form.get('sd'), request.form.get('ed')])


@app.route('/performance', methods=['GET', 'POST'])
def performance_bots():
    binfo = request.form.get('bots')
    s_date = request.form.get('sd')
    e_date = request.form.get('ed')
    if None in [binfo, s_date, e_date]:
        graph = '{{}}'
        title = "Graphing strategy"
    else:
        if s_date != '':
            s_date = parser.parse(s_date)
        if e_date != '':
            e_date = parser.parse(e_date)
        bname, strat_id = binfo.split('.')
        df, coin_id = results_query(s_date, e_date, strat_id)
        if not coin_id:
            return "<h1>Coin id not in strategies.parameters with strategy_id = %s</h1>" % strat_id
        binance_df = records_query(s_date, e_date, coin_id[0])
        df = binance_df.merge(df, on='timestamp', )
        resist = go.Scatter(x=df['timestamp'].tolist(), y=df['resist'].tolist(), name='Myopic_resistance')
        binance = go.Scatter(x=df['timestamp'].tolist(), y=df['values'].tolist(), name='Binance')
        support = go.Scatter(x=df['timestamp'].tolist(), y=df['support'].tolist(), name='Myopic_support')
        graph = json.dumps([resist, binance, support], cls=plotly.utils.PlotlyJSONEncoder)
        title = "%s, strategy: %s, coin: %s" % (bname, strat_id, list(coins.keys())[list(coins.values()).index(coin_id[0])])
    if (s_date == '' and e_date == '') or (s_date is None and e_date is None):
        s_date = datetime.datetime.today()
        e_date = datetime.datetime.today() + datetime.timedelta(days=1)

    return render_template('content.html', bots=bots, graph=graph, task='performance', title=title,
                           dates=[s_date.strftime("%Y-%m-%d"), e_date.strftime("%Y-%m-%d")])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
