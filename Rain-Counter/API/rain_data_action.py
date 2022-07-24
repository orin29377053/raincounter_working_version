from re import I
from datetime import datetime, timedelta
import psycopg2
import psycopg2.extras
import requests
import json
import pandas as pd
import time
import os
import hashlib
import subprocess

S_hostIP = ""
try:
    S_hostIP = os.getenv('raincounter_db_ip')
except:
    S_hostIP = ""


def update_raincounter_eq(x, y, voltage, device):
    pgdb_config = {
        'host': S_hostIP,
        'port': 15568,
        'user': 'CatIsCute',
        'password': 'raincounter',
        'database': 'CatIsCute', }
    try:
        print('update_raincounter_eq '+device+' start')

        sqls = (
            """  
                    UPDATE public."raincounter_equipment_db"  SET (x, y, voltage) = ('{x}','{y}','{voltage}') WHERE device = '{device}'
                """.format(
                x=x,
                y=y,                
                voltage=voltage,
                device=device)
        )
        print('update_raincounter_eq '+device+' success')

    except:
        print('update_raincounter_eq '+device+' error')
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(sqls)
    conn.commit()
    conn.close()

def update_time_raincounter_eq(last_update, device):
    pgdb_config = {
        'host': S_hostIP,
        'port': 15568,
        'user': 'CatIsCute',
        'password': 'raincounter',
        'database': 'CatIsCute', }
    try:
        print('update_time_raincounter_eq '+device+' start')

        sqls = (
            """  
                    UPDATE public."raincounter_equipment_db"  SET last_update = '{last_update}' WHERE device = '{device}'
                """.format(
                last_update=last_update,
                device=device
            )
        )
        print('update_time_raincounter_eq '+device+' success')
        with open("DEBUG_{}.txt".format(last_update.strftime("%Y%m%d-%H%M%S")), 'a') as f:
            f.write(            """  
                    UPDATE public."raincounter_equipment_db"  SET last_update = '{last_update}' WHERE device = '{device}'
                """.format(
                last_update=last_update,
                device=device
            )
            )


    except Exception as e:
        with open("DEBUG_{}.txt".format(last_update.strftime("%Y%m%d-%H%M%S")), 'a') as f:
            f.write(str(e))


        print('update_time_raincounter_eq '+device+' error')
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(sqls)
    conn.commit()
    conn.close()


    
def get_data_from_pgdb(device, start_time, end_time):
    # print('HIIIIIIII')
    from datetime import datetime, timedelta

    # 以使用者時區做時區處理 先-8
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    start_time = start_time-timedelta(hours=0)
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    end_time = end_time-timedelta(hours=0)
    print(start_time)
    print(end_time)
    # 出來是count
    # 只做時間處理
    pgdb_config = {
        'host': S_hostIP,
        'port': 15568,
        'user': 'CatIsCute',
        'password': 'raincounter',
        'database': 'CatIsCute',
    }
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sqls = ("""SELECT count_datetime,voltage,temp,count,upload_datetime,device,x,y
    FROM public.raindata
    
    WHERE device = '{device}' and count_datetime BETWEEN '{start_time}' and '{end_time}' 
    """).format(start_time=start_time,
                end_time=end_time,
                device=device)
    cursor.execute(sqls)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    print('ddd')
    df = pd.DataFrame(result)
    print(df)
    df = df.rename(columns={0: "time", 1: 'voltage', 2: 'temp',
        3: 'count', 4: 'upload_datetime', 5: 'device', 6: 'x', 7: 'y'})
    df['time'] = pd.to_datetime(df['time'])
    print(df)
    df_time = df.set_index('time')
    # 以使用者時區做時區處理 再+8

    df_time.index = df_time.index+timedelta(hours=0)

    return df_time


def min_raindata_to_hour(df_time):
    device = df_time.device.unique()[0]
    df_time = df_time.resample('min').mean()
    df_time_other = df_time.resample('H', closed='right', label='right').mean()
    df_time_rain = df_time.resample('H', closed='right', label='right').sum()
    df_time_other['count'] = df_time_rain['count']
    df_time_other['device'] = device
    df_time_other['rainfall'] = df_time_other['count']*0.2
    df_time_other['time'] = df_time_other.index
    df_time_other = df_time_other.fillna(value=float(-333))
    return df_time_other


def min_raindata_to_10min(df_time):
    device = df_time.device.unique()[0]
    df_time = df_time.resample('min').mean()
    df_time_other = df_time.resample(
        '10T', closed='right', label='right').mean()
    df_time_rain = df_time.resample('10T', closed='right', label='right').sum()
    df_time_other['count'] = df_time_rain['count']
    df_time_other['device'] = device
    df_time_other['rainfall'] = df_time_other['count']*0.2
    df_time_other['time'] = df_time_other.index
    df_time_other = df_time_other.fillna(value=float(-333))
    return df_time_other


def min_raindata_to_Day(df_time):
    device = df_time.device.unique()[0]
    df_time = df_time.resample('min').mean()
    df_time_other = df_time.resample('D', closed='right', label='left').mean()
    df_time_rain = df_time.resample('D', closed='right', label='left').sum()
    df_time_other['count'] = df_time_rain['count']
    df_time_other['device'] = device
    df_time_other['rainfall'] = df_time_other['count']*0.2
    df_time_other['time'] = df_time_other.index
    return df_time_other


def update_raincounter_rain_info(device):
    print('update_raincounter_rain_info '+device+' start')
    start_time = datetime.strftime(datetime.strptime(datetime.strftime(datetime.now(
    ), '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')-timedelta(hours=64), '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strftime(datetime.strptime(datetime.strftime(datetime.now(
        ), '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')+timedelta(hours=8), '%Y-%m-%d %H:%M:%S')
    try:
        df = get_data_from_pgdb(device, start_time, end_time)
        df_H = min_raindata_to_hour(df)
        print(len(df_H))
        df_M = min_raindata_to_10min(df)
        #print(df_M)
        pgdb_config = {
            'host': S_hostIP,
            'port': 15568,
            'user': 'CatIsCute',
            'password': 'raincounter',
            'database': 'CatIsCute', }
        if len(df_M) > 10:
            td = end_time[:10]
            try:
                M10 = df_M.iloc[-1]['rainfall']
                #print(M10)
                sqls = (
                    """  
                            UPDATE public."raincounter_equipment_db"  SET "10min" = '{M10}' WHERE device = '{device}'
                        """.format(
                        M10=M10,
                        device=device)
                )
                conn = psycopg2.connect(**pgdb_config)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(sqls)
                conn.commit()
                conn.close()
            except:
                print('update_raincounter_rain_info '+device+'10min data error')
            try:
                H = df_H.iloc[-1]['rainfall']
                sqls = (
                    """  
                            UPDATE public."raincounter_equipment_db"  SET "60min" = '{H}' WHERE device = '{device}'
                        """.format(
                        H=H,
                        device=device)
                )
                conn = psycopg2.connect(**pgdb_config)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(sqls)
                conn.commit()
                conn.close()
            except:
                print('update_raincounter_rain_info '+device+'60min data error')

            try:
                H3 = df_H.iloc[-3:]['rainfall'].sum()
                sqls = (
                    """  
                            UPDATE public."raincounter_equipment_db"  SET "3h" = '{H3}' WHERE device = '{device}'
                        """.format(
                        H3=H3,
                        device=device)
                )
                conn = psycopg2.connect(**pgdb_config)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(sqls)
                conn.commit()
                conn.close()
            except:
                print('update_raincounter_rain_info '+device+'3H data error')

            try:
                H6 = df_H.iloc[-6:]['rainfall'].sum()
                sqls = (
                    """  
                            UPDATE public."raincounter_equipment_db"  SET "6h" = '{H6}' WHERE device = '{device}'
                        """.format(
                        H6=H6,
                        device=device)
                )
                conn = psycopg2.connect(**pgdb_config)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(sqls)
                conn.commit()
                conn.close()
            except:
                print('update_raincounter_rain_info '+device+'6H data error')

            try:
                H12 = df_H.iloc[-12:]['rainfall'].sum()
                sqls = (
                    """  
                            UPDATE public."raincounter_equipment_db"  SET "12h" = '{H12}' WHERE device = '{device}'
                        """.format(
                        H12=H12,
                        device=device)
                )
                conn = psycopg2.connect(**pgdb_config)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(sqls)
                conn.commit()
                conn.close()
            except:
                print('update_raincounter_rain_info '+device+'12H data error')

            try:
                H24 = df_H.iloc[-24:]['rainfall'].sum()
                sqls = (
                    """  
                            UPDATE public."raincounter_equipment_db"  SET "24h" = '{H24}' WHERE device = '{device}'
                        """.format(
                        H24=H24,
                        device=device)
                )
                conn = psycopg2.connect(**pgdb_config)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(sqls)
                conn.commit()
                conn.close()
                print('update_raincounter_rain_info '+device+'H24 data OK')
            except:
                print('update_raincounter_rain_info '+device+'H24 data error')

            try:
                today = df_H[td:]['rainfall'].sum()
                sqls = (
                    """  
                            UPDATE public."raincounter_equipment_db"  SET "today" = '{today}' WHERE device = '{device}'
                        """.format(
                        today=today,
                        device=device)
                )
                conn = psycopg2.connect(**pgdb_config)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(sqls)
                conn.commit()
                conn.close()
            except:
                print('update_raincounter_rain_info '+device+'today data error')

            try:
                H48 = df_H.iloc[-48:]['rainfall'].sum()
                sqls = (
                    """  
                            UPDATE public."raincounter_equipment_db"  SET "48h" = '{H48}' WHERE device = '{device}'
                        """.format(
                        H48=H48,
                        device=device)
                )
                conn = psycopg2.connect(**pgdb_config)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(sqls)
                conn.commit()
                conn.close()
            except:
                print('update_raincounter_rain_info '+device+'48H data error')

            try:
                H72 = df_H.iloc[-72:]['rainfall'].sum()
                sqls = (
                    """  
                            UPDATE public."raincounter_equipment_db"  SET "72h" = '{H72}' WHERE device = '{device}'
                        """.format(
                        H72=H72,
                        device=device)
                )
                conn = psycopg2.connect(**pgdb_config)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(sqls)
                conn.commit()
                conn.close()
            except:
                print('update_raincounter_rain_info '+device+'72H data error')
            print('update_raincounter_rain_info '+device+' success')
        else:
            print('update_raincounter_rain_info '+device+' error')
    except:
        print('update_raincounter_rain_info '+device+' error')



def check_eq_is_exist(device):
    print('check_eq_is_exist '+device+' start')

    pgdb_config={
            'host':S_hostIP,
            'port':15568,
            'user':'CatIsCute',
            'password':'raincounter',
            'database':'CatIsCute',    }

    sqls=(
            """  
                INSERT INTO public."raincounter_equipment_db"(device,status)
                VALUES('{device}','unregister')
                ON conflict(device) DO NOTHING
            """.format(device=device)
            ) 
    try:
        conn = psycopg2.connect(**pgdb_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sqls)
        conn.commit()
        conn.close()
        print('check_eq_is_exist '+device+' success')
    except:
        print(device,' check_eq_is_exist_error')


def upload_mode_update(device):
    print('upload_mode_update '+device+' start')
    pgdb_config = {
    'host': S_hostIP,
    'port': 15568,
    'user': 'CatIsCute',
    'password': 'raincounter',
    'database': 'CatIsCute', }
    sqls = (
        """  
                SELECT upload_mode FROM public."raincounter_equipment_db"
                where device='{device}'
            """.format(device=device)
    )
    try:
        conn = psycopg2.connect(**pgdb_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sqls)
        print('upload_mode_update '+device+' start2')

        upload_mode = cursor.fetchall()[0][0]
        print(upload_mode)
        #print('upload_mode_update '+device +'success and up loadmode is' +str(upload_mode)+' min')
        
    except:
        print('upload_mode_update '+device+' error')
        upload_mode = 5

    return upload_mode

def get_device_name(device):
    pgdb_config={
        'host':S_hostIP,
        'port':15568,
        'user':'CatIsCute',
        'password':'raincounter',
        'database':'CatIsCute',
        }
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sqls = ("""SELECT name FROM public.raincounter_equipment_db
    WHERE device = '{device}'  
    """).format(device=device)           
    cursor.execute(sqls)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    name=result[0][0]
    return name
