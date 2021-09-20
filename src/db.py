import psycopg2
import pandas as pd
# query = 'SELECT "timestamp", coin_id, "open", high, low, "close", volume, quote_av, trades, tb_base_av, tb_quote_av, "ignore", dumptime, datasource_id FROM prices.coins;'

query = 'SELECT ' \
        '"timestamp", "close" ' \
        'FROM prices.coins ' \
        'where coin_id=%d ' \
        'ORDER BY TIMESTAMP DESC LIMIT 100;'

# class postgres():
#     def __init__(self):

def get_connection():
    return psycopg2.connect(user="postgres",
                                  password="august!2021",
                                  host="172.31.20.145",
                                  port="5432",
                                  database="production")


def last_binance(coin):
    connection = get_connection()
    if not connection: raise Exception('Connection Error')
    cursor = connection.cursor()
    cursor.execute(query % coin)
    res = cursor.fetchall()
    cursor.close()
    connection.close()
    return pd.DataFrame(res, columns=['timestamp', 'values'])

