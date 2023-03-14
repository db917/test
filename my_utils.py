import cx_Oracle
import pymysql
import pandas as pd
import requests
'''
oracle
'''

dsn = cx_Oracle.makedsn('localhost', 1521, 'xe')
seoul_api_key = '704f705467656d72343047476d4569'
riot_api_key = 'RGAPI-4b2560bc-188a-4014-b53f-81acae2bdd70'

def db_open():
    global db
    global cursor
    db = cx_Oracle.connect(user='ICIA', password='1234', dsn=dsn)
    cursor = db.cursor()
    print('oracle open!!')


def oracle_execute(q):
    global db
    global cursor
    try:
        if 'SELECT' in q or 'select' in q:
            df = pd.read_sql(sql=q, con=db)
            return df
        cursor.execute(q)
        return 'oracle query 성공'
    except Exception as e:
        print(e)


def oracle_close():
    global db
    global cursor
    try:
        db.commit()
        cursor.close()
        db.close()
        return 'oracle close'
    except Exception as e:
        print(e)


'''
mysql
'''


def connect_mysql(db):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db=db, charset='utf8')
    return conn

def mysql_execute(query, conn):
    cursor_mysql = conn.cursor()
    cursor_mysql.execute(query)
    result = cursor_mysql.fetchall()
    return result

def mysql_execute_dict(query, conn):
    cursor_mysql = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor_mysql.execute(query)
    result = cursor_mysql.fetchall()
    return result

def df_creater(url):
    url = url.replace('(인증키)', seoul_api_key).replace('xml', 'json').replace('/5/', '/1000/')
    res = requests.get(url).json()
    key = list(res.keys())[0]
    data = res[key]['row']
    df = pd.DataFrame(data)
    return df


def get_puuid(user):
    url = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{user}?api_key={riot_api_key}'
    res = requests.get(url).json()
    puuid = res['puuid']
    return puuid


def get_match_id(puuid,num):
    url = f'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={num}&api_key={riot_api_key}'
    match_id = requests.get(url).json()
    return match_id


def get_matches_timelines(match_id):
    url1 = f'https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={riot_api_key}'
    res1 = requests.get(url1).json()
    url2 = f'https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline?api_key={riot_api_key}'
    res2 = requests.get(url2).json()
    return res1, res2

print('git tests')