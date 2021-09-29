import psycopg2
import pandas as pd
import datetime
# query = 'SELECT "timestamp", coin_id, "open", high, low, "close", volume, quote_av, trades, tb_base_av, tb_quote_av, "ignore", dumptime, datasource_id FROM prices.coins;'

query = 'SELECT ' \
        '"timestamp", "close" ' \
        'FROM prices.coins p ' \
        "where p.coin_id='%d' AND p.timestamp >= '%s' AND p.timestamp <= '%s'" \
        'ORDER BY p.timestamp DESC;'
"SELECT * FROM prices.coins p where p.timestamp >= '2021-01-01' and p.timestamp <= '2021-04-02' limit 20;"
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
        s_date = datetime.datetime.today() - datetime.timedelta(days=1)
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

