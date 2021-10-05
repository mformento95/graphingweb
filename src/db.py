import psycopg2
import pandas as pd
import datetime

# query = 'SELECT "timestamp", coin_id, "open", high, low, "close", volume, quote_av, trades, tb_base_av, tb_quote_av, "ignore", dumptime, datasource_id FROM prices.coins;'

query = 'SELECT "timestamp", "close" ' \
        'FROM prices.coins p ' \
        "where p.coin_id='%d' AND p.timestamp >= '%s' AND p.timestamp <= '%s'" \
        'ORDER BY p.timestamp DESC;'

results = "SELECT timestamp, features -> 'myopic_resist' as resist, features -> 'myopic_support' as support" \
          " FROM strategies.results" \
          " where strategy_id = '%s' and timestamp >= '%s' AND timestamp <= '%s';"

strategy_coin = "SELECT setup_info ->  'coin_id' from strategies.parameters where strategy_id = '%s';"

# class postgres():
#     def __init__(self):

def get_connection():
    return psycopg2.connect(user="postgres",
                            password="august!2021",
                            host="172.31.20.145",
                            port="5432",
                            database="production")


def records_query(s_date, e_date, coin):
    if s_date == '':
        s_date = datetime.datetime.today()
    if e_date == '':
        e_date = datetime.datetime.today() + datetime.timedelta(days=1)
    connection = get_connection()
    if not connection: raise Exception('Connection Error')
    cursor = connection.cursor()
    cursor.execute(query % (coin, s_date.strftime("%Y-%m-%d"), e_date.strftime("%Y-%m-%d")))
    res = cursor.fetchall()
    cursor.close()
    connection.close()
    return pd.DataFrame(res, columns=['timestamp', 'values'])


def results_query(s_date, e_date, strat_id):
    if s_date == '':
        s_date = datetime.datetime.today()
    if e_date == '':
        e_date = datetime.datetime.today() + datetime.timedelta(days=1)
    connection = get_connection()
    if not connection: raise Exception('Connection Error')
    cursor = connection.cursor()
    cursor.execute(results % (strat_id, s_date.strftime("%Y-%m-%d"), e_date.strftime("%Y-%m-%d")))
    res = cursor.fetchall()
    cursor.execute(strategy_coin % strat_id)
    coin_id = cursor.fetchall()
    cursor.close()
    connection.close()
    return pd.DataFrame(res, columns=['timestamp', 'resist', 'support']), coin_id[0] if len(coin_id[0]) > 0 else None
