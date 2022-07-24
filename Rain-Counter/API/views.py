from django.shortcuts import render
from re import I
from datetime import datetime, timedelta
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
import psycopg2
import psycopg2.extras
import requests
import json
import pandas as pd
import time
import os
import hashlib
import subprocess
from . import rain_data_action
import lineBotFunction
from django.http.request import QueryDict, MultiValueDict
from django.core.files.temp import NamedTemporaryFile
from django.http import FileResponse
from ipware import get_client_ip
import logging
logger = logging.getLogger('django')

#################################
# LINR BOT Tset
#################################
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
LINE_CHANNEL_ACCESS_TOKEN = '1657065204'
LINE_CHANNEL_SECRET = '2461cdaa50bfcd0c4fc21964fef1b115'
LineBot_ = lineBotFunction.LineBotMessage()


#################################
# LINR BOT Tset
#################################
S_hostIP = ""
try:
    S_hostIP = os.getenv('raincounter_db_ip')
except:
    S_hostIP = ""
# Create your views here.
pgdb_config = {
    'host': S_hostIP,
    'port': '15568',
    'user': 'CatIsCute',
    'password': 'raincounter',
    'database': 'CatIsCute',
}

# page add by wenny


def hello_world(request):
    return render(request, 'index.html')


def equipment(request):
    return render(request, 'instrument.html')


def heatmapo(request):
    return render(request, 'heatmap.html')


def heatmap(request):
    return render(request, 'heatmap.html')

# Create your views here.
# hiiii


# def update_raincounter_eq(x, y, voltage, device):
#     pgdb_config = {
#         'host': '140.112.152.49',
#         'port': 5568,
#         'user': 'CatIsCute',
#         'password': 'raincounter',
#         'database': 'CatIsCute', }
#     try:
#         sqls = (
#             """  
#                     UPDATE public."raincounter_equipment_db"  SET (x, y, voltage) = ('{x}','{y}','{voltage}') WHERE device = '{device}'
#                 """.format(
#                 x=x,
#                 y=y,                
#                 voltage=voltage,
#                 device=device)
#         )
#     except:
#         print('update_raincounter_eq '+device+' error')
#     conn = psycopg2.connect(**pgdb_config)
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cursor.execute(sqls)
#     conn.commit()
#     conn.close()


# def update_time_raincounter_eq(last_update, device):
#     pgdb_config = {
#         'host': '140.112.152.49',
#         'port': 5568,
#         'user': 'CatIsCute',
#         'password': 'raincounter',
#         'database': 'CatIsCute', }
#     try:
#         sqls = (
#             """  
#                     UPDATE public."raincounter_equipment_db"  SET last_update = '{last_update}' WHERE device = '{device}'
#                 """.format(
#                 last_update=last_update,
#                 device=device
#             )
#         )
#     except:
#         print('update_time_raincounter_eq '+device+' error')
#     conn = psycopg2.connect(**pgdb_config)
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cursor.execute(sqls)
#     conn.commit()
#     conn.close()


# def get_data_from_pgdb(device, start_time, end_time):
#     # print('HIIIIIIII')
#     from datetime import datetime, timedelta

#     # 以使用者時區做時區處理 先-8
#     start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
#     start_time = start_time-timedelta(hours=8)
#     end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
#     end_time = end_time-timedelta(hours=8)

#     # 出來是count
#     # 只做時間處理
#     pgdb_config = {
#         'host': '140.112.152.49',
#         'port': 5568,
#         'user': 'CatIsCute',
#         'password': 'raincounter',
#         'database': 'CatIsCute',
#     }
#     conn = psycopg2.connect(**pgdb_config)
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     sqls = ("""SELECT count_datetime,voltage,temp,count,upload_datetime,device,x,y
#     FROM public.raindata
    
#     WHERE device = '{device}' and count_datetime BETWEEN '{start_time}' and '{end_time}' 
#     """).format(start_time=start_time,
#                 end_time=end_time,
#                 device=device)
#     cursor.execute(sqls)
#     result = cursor.fetchall()
#     conn.commit()
#     conn.close()
#     df = pd.DataFrame(result)
#     df = df.rename(columns={0: "time", 1: 'voltage', 2: 'temp',
#         3: 'count', 4: 'upload_datetime', 5: 'device', 6: 'x', 7: 'y'})
#     df['time'] = pd.to_datetime(df['time'])
#     df_time = df.set_index('time')
#     # 以使用者時區做時區處理 再+8

#     df_time.index = df_time.index+timedelta(hours=8)
#     return df_time


# def min_raindata_to_hour(df_time):
#     device = df_time.device.unique()[0]
#     df_time = df_time.resample('min').mean()
#     df_time_other = df_time.resample('H', closed='right', label='right').mean()
#     df_time_rain = df_time.resample('H', closed='right', label='right').sum()
#     df_time_other['count'] = df_time_rain['count']
#     df_time_other['device'] = device
#     df_time_other['rainfall'] = df_time_other['count']*0.2
#     df_time_other['time'] = df_time_other.index
#     df_time_other = df_time_other.fillna(value=float(-333))
#     return df_time_other


# def min_raindata_to_10min(df_time):
#     device = df_time.device.unique()[0]
#     df_time = df_time.resample('min').mean()
#     df_time_other = df_time.resample(
#         '10T', closed='right', label='right').mean()
#     df_time_rain = df_time.resample('10T', closed='right', label='right').sum()
#     df_time_other['count'] = df_time_rain['count']
#     df_time_other['device'] = device
#     df_time_other['rainfall'] = df_time_other['count']*0.2
#     df_time_other['time'] = df_time_other.index
#     df_time_other = df_time_other.fillna(value=float(-333))
#     return df_time_other


# def min_raindata_to_Day(df_time):
#     device = df_time.device.unique()[0]
#     df_time = df_time.resample('min').mean()
#     df_time_other = df_time.resample('D', closed='right', label='left').mean()
#     df_time_rain = df_time.resample('D', closed='right', label='left').sum()
#     df_time_other['count'] = df_time_rain['count']
#     df_time_other['device'] = device
#     df_time_other['rainfall'] = df_time_other['count']*0.2
#     df_time_other['time'] = df_time_other.index
#     return df_time_other


# def update_raincounter_rain_info(device):
#     print('update_raincounter_rain_info start')
#     start_time = datetime.strftime(datetime.strptime(datetime.strftime(datetime.now(
#     ), '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')-timedelta(hours=64), '%Y-%m-%d %H:%M:%S')
#     end_time = datetime.strftime(datetime.strptime(datetime.strftime(datetime.now(
#         ), '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')+timedelta(hours=8), '%Y-%m-%d %H:%M:%S')
#     df = rain_data_action.get_data_from_pgdb(device, start_time, end_time)
#     df_H = rain_data_action.min_raindata_to_hour(df)
#     print(len(df_H))
#     df_M = min_raindata_to_10min(df)
#     #print(df_M)
#     pgdb_config = {
#         'host': '140.112.152.49',
#         'port': 5568,
#         'user': 'CatIsCute',
#         'password': 'raincounter',
#         'database': 'CatIsCute', }
#     if len(df_M) > 10:
#         td = end_time[:10]
#         try:
#             M10 = df_M.iloc[-1]['rainfall']
#             #print(M10)
#             sqls = (
#                 """  
#                         UPDATE public."raincounter_equipment_db"  SET "10min" = '{M10}' WHERE device = '{device}'
#                     """.format(
#                     M10=M10,
#                     device=device)
#             )
#             conn = psycopg2.connect(**pgdb_config)
#             cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#             cursor.execute(sqls)
#             conn.commit()
#             conn.close()
#         except:
#             print('update_raincounter_rain_info '+device+'10min data error')
#         try:
#             H = df_H.iloc[-1]['rainfall']
#             sqls = (
#                 """  
#                         UPDATE public."raincounter_equipment_db"  SET "60min" = '{H}' WHERE device = '{device}'
#                     """.format(
#                     H=H,
#                     device=device)
#             )
#             conn = psycopg2.connect(**pgdb_config)
#             cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#             cursor.execute(sqls)
#             conn.commit()
#             conn.close()
#         except:
#             print('update_raincounter_rain_info '+device+'60min data error')

#         try:
#             H3 = df_H.iloc[-3:]['rainfall'].sum()
#             sqls = (
#                 """  
#                         UPDATE public."raincounter_equipment_db"  SET "3h" = '{H3}' WHERE device = '{device}'
#                     """.format(
#                     H3=H3,
#                     device=device)
#             )
#             conn = psycopg2.connect(**pgdb_config)
#             cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#             cursor.execute(sqls)
#             conn.commit()
#             conn.close()
#         except:
#             print('update_raincounter_rain_info '+device+'3H data error')

#         try:
#             H6 = df_H.iloc[-6:]['rainfall'].sum()
#             sqls = (
#                 """  
#                         UPDATE public."raincounter_equipment_db"  SET "6h" = '{H6}' WHERE device = '{device}'
#                     """.format(
#                     H6=H6,
#                     device=device)
#             )
#             conn = psycopg2.connect(**pgdb_config)
#             cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#             cursor.execute(sqls)
#             conn.commit()
#             conn.close()
#         except:
#             print('update_raincounter_rain_info '+device+'6H data error')

#         try:
#             H12 = df_H.iloc[-12:]['rainfall'].sum()
#             sqls = (
#                 """  
#                         UPDATE public."raincounter_equipment_db"  SET "12h" = '{H12}' WHERE device = '{device}'
#                     """.format(
#                     H12=H12,
#                     device=device)
#             )
#             conn = psycopg2.connect(**pgdb_config)
#             cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#             cursor.execute(sqls)
#             conn.commit()
#             conn.close()
#         except:
#             print('update_raincounter_rain_info '+device+'12H data error')

#         try:
#             H24 = df_H.iloc[-24:]['rainfall'].sum()
#             sqls = (
#                 """  
#                         UPDATE public."raincounter_equipment_db"  SET "24h" = '{H24}' WHERE device = '{device}'
#                     """.format(
#                     H24=H24,
#                     device=device)
#             )
#             conn = psycopg2.connect(**pgdb_config)
#             cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#             cursor.execute(sqls)
#             conn.commit()
#             conn.close()
#             print('update_raincounter_rain_info '+device+'H24 data OK')
#         except:
#             print('update_raincounter_rain_info '+device+'H24 data error')

#         try:
#             today = df_H[td:]['rainfall'].sum()
#             sqls = (
#                 """  
#                         UPDATE public."raincounter_equipment_db"  SET "today" = '{today}' WHERE device = '{device}'
#                     """.format(
#                     today=today,
#                     device=device)
#             )
#             conn = psycopg2.connect(**pgdb_config)
#             cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#             cursor.execute(sqls)
#             conn.commit()
#             conn.close()
#         except:
#             print('update_raincounter_rain_info '+device+'today data error')

#         try:
#             H48 = df_H.iloc[-48:]['rainfall'].sum()
#             sqls = (
#                 """  
#                         UPDATE public."raincounter_equipment_db"  SET "48h" = '{H48}' WHERE device = '{device}'
#                     """.format(
#                     H48=H48,
#                     device=device)
#             )
#             conn = psycopg2.connect(**pgdb_config)
#             cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#             cursor.execute(sqls)
#             conn.commit()
#             conn.close()
#         except:
#             print('update_raincounter_rain_info '+device+'48H data error')

#         try:
#             H72 = df_H.iloc[-72:]['rainfall'].sum()
#             sqls = (
#                 """  
#                         UPDATE public."raincounter_equipment_db"  SET "72h" = '{H72}' WHERE device = '{device}'
#                     """.format(
#                     H72=H72,
#                     device=device)
#             )
#             conn = psycopg2.connect(**pgdb_config)
#             cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#             cursor.execute(sqls)
#             conn.commit()
#             conn.close()
#         except:
#             print('update_raincounter_rain_info '+device+'72H data error')

# def check_eq_is_exist(device):
#     pgdb_config={
#             'host':'140.112.152.49',
#             'port':5568,
#             'user':'CatIsCute',
#             'password':'raincounter',
#             'database':'CatIsCute',    }

#     sqls=(
#             """  
#                 INSERT INTO public."raincounter_equipment_db"(device,status)
#                 VALUES('{device}','unregister')
#                 ON conflict(device) DO NOTHING
#             """.format(device=device)
#             ) 
#     try:
#         conn = psycopg2.connect(**pgdb_config)
#         cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cursor.execute(sqls)
#         conn.commit()
#         conn.close()
#         print(device,' check_eq_is_exist')
#     except:
#         print(device,' check_eq_is_exist_error')

# def upload_mode_update(device):
#     pgdb_config = {
#     'host': '140.112.152.49',
#     'port': 5568,
#     'user': 'CatIsCute',
#     'password': 'raincounter',
#     'database': 'CatIsCute', }
#     sqls = (
#         """  
#                 SELECT upload_mode FROM public."raincounter_equipment_db"
#                 where device='{device}'
#             """.format(device=device)
#     )
#     conn = psycopg2.connect(**pgdb_config)
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cursor.execute(sqls)
#     upload_mode = cursor.fetchall()[0][0]
#     return upload_mode



@api_view(['GET'])
def apioverview(request):
    api_urls = {
        'upload': '/data_upload/',
    }
    return JsonResponse(api_urls)


@api_view(['Post'])
def data_upload(request):
    data = (request.headers['data'])  # .split(',')
    data = json.loads(data)
    device = data[0]
    count = data[1]
    x = data[2]
    y = data[3]
    count_datetime = data[4]
    voltage = data[5]
    update_by = data[6]
    sqls = (
        """  
                INSERT INTO raindata 
                (device, count, x, y, count_datetime, voltage, update_by)
                VALUES 
                ('{device}', '{count}', '{x}', '{y}', '{count_datetime}','{voltage}','{update_by}')
            """.format(
            device=device,
            count=count,
            x=x,
            y=y,
            count_datetime=count_datetime,
            voltage=voltage,
            update_by=update_by,
        )
    )
    print(sqls)
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(sqls)
    conn.commit()
    conn.close()
    return Response('nice!')


@api_view(['GET', 'POST'])
def data_upload_iot(request):
    logger.info("Get HTTP requets from IOT")
    S_errorLog = ""
    try:
        S_errorLog += str(request.headers)
        S_errorLog += "\r\n"
        S_errorLog += str(request.body)
        S_errorLog += "\r\n"
        S_bodyPostGet = request.body.decode('utf-8')
        if len(S_bodyPostGet) != 0:
            raw_data = S_bodyPostGet
            if (request.headers.get("Datas", None) != None):
                D_headerData = json.loads(request.headers['Datas'].replace("'",'"'))
                device = D_headerData["ID"]
                logger.info("ID: {}".format(device))
                try:
                    Firmware = D_headerData["Firmware"]
                except:
                    Firmware = "0"
                logger.info("Firmware: {}".format(Firmware))
                try:
                    GMT = int(D_headerData["GMT"])
                except:
                    GMT = 0
                logger.info("GMT: {}".format(GMT))
                S_MD5 = D_headerData["MD5"]
                logger.info("IOT S_MD5: {}".format(S_MD5))
                m = hashlib.md5()
                m.update(raw_data.encode('utf-8'))
                h = m.hexdigest()
                logger.info("Server MD5: {}".format(h))
                if h != S_MD5:
                    logger.error("MD5 not match! Fail")
                    S_getMD5FailCountByID = '''
                        SELECT md5_fail_count FROM public.raincounter_equipment_db
                        WHERE device='{}'
                    '''.format(device)
                    conn = psycopg2.connect(**pgdb_config)
                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                    cursor.execute(S_getMD5FailCountByID)
                    result = cursor.fetchall()
                    conn.commit()
                    conn.close()
                    if result:
                        if result[0][0] >= 20:
                            # 若md5連續20次比對失敗 就讓資料上傳直接過 避免永遠塞車
                            logger.warning("device ID: accumulate more than 20 failures".format(device))
                        else:
                            logger.warning("MD5 fail count: {}".format(result[0][0] + 1))
                            S_resetMD5FailCount = '''
                                UPDATE raincounter_equipment_db 
                                SET md5_fail_count = {}
                                WHERE device='{}'
                            '''.format(result[0][0] + 1, device)
                            conn = psycopg2.connect(**pgdb_config)
                            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                            cursor.execute(S_resetMD5FailCount)
                            conn.commit()
                            conn.close()


                            return HttpResponse(status=501)
                    else:
                        logger.error("device ID: has not logged in".format(device))
                        return HttpResponse(status=502)
                    

                S_resetMD5FailCount = '''
                    UPDATE raincounter_equipment_db 
                    SET md5_fail_count = 0
                    WHERE device='{}'
                '''.format(device)
                conn = psycopg2.connect(**pgdb_config)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(S_resetMD5FailCount)
                conn.commit()
                conn.close()

                # s_MESSAGE = "測試訊息: {} 收到資料了".format(device)
                # LineBot_.SendToCatWindow(s_MESSAGE)
                S_dataSavePath = "./dataGet/{}".format(device)
                logger.info("S_dataSavePath: {}".format(S_dataSavePath))
                if (os.path.exists(S_dataSavePath) == False):
                    os.makedirs(S_dataSavePath)
                S_dataGetFilePath = "./dataGet/{}/{}.txt".format(device,S_MD5)
                logger.info("S_dataGetFilePath: {}".format(S_dataGetFilePath))
                with open(S_dataGetFilePath,'w') as f:                    
                    f.write(raw_data)
                logger.info("Data Save SUCCESS!")
                logger.info("Try to update upload_mode")
                try:
                    new_upload_mode=rain_data_action.upload_mode_update(device)
                    print(new_upload_mode)
                except:
                    logger.info("Update upload_mode fail")
                #new_upload_mode=1
                logger.info("ID: {} Data Upload Success!".format(device))
                S_filePath = os.path.join(os.path.split(os.path.realpath(__file__))[0],'..','writeDataIntoDB.py')
                # p = subprocess.Popen('python3 /home/sinotech_se39/myProject/Rain-Counter2/Rain-Counter/writeDataIntoDB.py --ID {}'.format(device))
                logger.info("Run: python3 {} --ID {} --GMT {}".format(S_filePath, device, GMT))
                p = subprocess.Popen(['python3',S_filePath,'--ID',device, '--GMT', "{}".format(GMT)])
                logger.info("Return HTTP Respone")
                return Response(',UpdateInterval = {0}'.format(new_upload_mode))

        else:
            logger.error("Dont have any data in body!")
            return HttpResponse(status=501)

        try:
            new_upload_mode=rain_data_action.upload_mode_update(device)
        except:
            logger.warning('new_upload_mode is error')
        #new_upload_mode=5
        return Response(',UpdateInterval = {0}'.format(new_upload_mode))
    except Exception as e:
        S_errorLog += str(e)
        logger.error(S_errorLog)
        # LineBot_.SendToCatWindow("Fail: {}".format(str(e)))

        # if device=='TestVersion_3':
        #     return Response(',UpdateInterval = 1')
        return HttpResponse(status=500)


@api_view(['GET'])
def data_get_test(request):
    sqls = (
        """  
                SELECT json_agg (raindata) FROM raindata WHERE  device = 'test';
                
            """
    )
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(sqls)
    data = cursor.fetchall()
    #jsonObj = json.dumps(data[0][0])
    print(type(data[0][0]))
    conn.commit()
    conn.close()
    return JsonResponse(data[0][0], safe=False)
    # return HttpResponse(json.dumps(data[0][0]), content_type = "application/json")
    # ,json_dumps_params=None


@api_view(['GET'])
def get_raincounter_eq(request):
    queryparams = request.query_params
    print(queryparams)
    pgdb_config = {
        'host': S_hostIP,
        'port': 15568,
        'user': 'CatIsCute',
        'password': 'raincounter',
        'database': 'CatIsCute', }
    sqls = (
        """  
                SELECT json_agg (raincounter_equipment_db ORDER BY id) FROM public."raincounter_equipment_db"
            """
    )
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(sqls)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return JsonResponse(data[0][0], safe=False)
    # return HttpResponse(json.dumps(data[0][0]), content_type = "application/json")
    # ,json_dumps_params=None


@api_view(['GET'])
def get_rain_data(request):
    queryparams = request.query_params
    device = queryparams['name']
    print(device)
    if 'start_time' in queryparams.keys():
        start_time = queryparams['start_time']
    else:
        start_time = datetime.strftime(datetime.strptime(datetime.strftime(datetime.now(
        ), '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')-timedelta(hours=64), '%Y-%m-%d %H:%M:%S')

    if 'end_time' in queryparams.keys():
        end_time = queryparams['end_time']
    else:
        end_time = datetime.strftime(datetime.strptime(datetime.strftime(datetime.now(
        ), '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')+timedelta(hours=8), '%Y-%m-%d %H:%M:%S')
    try:
        df = rain_data_action.get_data_from_pgdb(device, start_time, end_time)
        
        df = rain_data_action.min_raindata_to_hour(df)
        data = df.to_dict('records')
    except:
        data = 'error!!!'
    return JsonResponse(data, safe=False)
    # SELECT json_agg (raindata) FROM raindata WHERE  device = 'test';
    # http://140.112.152.49:5566/api/get_rain_data/?name=TestVersion_3&start_time=2022-04-09 00:00:00&end_time=2022-04-12 00:00:00


#################################
# LINR BOT Tset API
#################################

def line_bot_get(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                print("OK")
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def sslFileReturn(request):
    content = """F25268D6A2F09EF0BF8A220F93614C59A7EAC44A6A5562092C157C1D260BB026
comodoca.com
61f86b0c764b627"""
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        "E766DCF1B288D001709AAD99F579406C.txt")
    return response
#################################
# LINR BOT Tset API
#################################
    # SELECT json_agg (raindata) FROM raindata WHERE  device = 'test';
    # http://140.112.152.49:5566/api/get_rain_data/?name=TestVersion_3&start_time=2022-04-09 00:00:00&end_time=2022-04-12 00:00:00


@api_view(['GET'])
def update_raindata(request):
    queryparams = request.query_params
    print(queryparams)
    device = queryparams['name']

    rain_data_action.update_raincounter_rain_info(device)
    data = 'ok'

    return JsonResponse(data, safe=False)





@api_view(['POST'])
def revise_eq_info(request):
    
    try:
        data=QueryDict.dict(request.data)
        pwd=data['verify']
        if pwd=='0911':
            ID=data['id']
            print('id is',ID)
            data.pop('id', None)
            data.pop('verify', None)
            keys=list(data.keys())
            if len(keys)==1:
                key=keys[0]
                value=data[key]
                pgdb_config={
                        'host':S_hostIP,
                        'port':15568,
                        'user':'CatIsCute',
                        'password':'raincounter',
                        'database':'CatIsCute',    }
                sqls=(
                                """  
                                update  public."raincounter_equipment_db"
                                set {key} = '{value}'
                                WHERE id = '{ID}'
                                """.format(
                                    key=key,
                                    value=value,
                                    ID=ID
                                )
                                )  
                conn = psycopg2.connect(**pgdb_config)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(sqls)    
                conn.commit()
                conn.close()
            else:
                keys_str = [i for i in keys]    
                keys_str = ' , '.join(keys_str)
                values=list(data.values())
                values_str=str(values)[1:][:-1]
                print(data)     
                # print(keys)
                # print(values)    
                pgdb_config={
                            'host':S_hostIP,
                            'port':15568,
                            'user':'CatIsCute',
                            'password':'raincounter',
                            'database':'CatIsCute',    }
                sqls=(
                                    """  
                                    update  public."raincounter_equipment_db"
                                    set ({keys}) = ({values})
                                    WHERE id = '{ID}'
                                    """.format(
                                        keys=keys_str,
                                        values=values_str,
                                        ID=ID
                                    )
                                    )  
            conn = psycopg2.connect(**pgdb_config)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(sqls)    
            conn.commit()
            conn.close()   
            # for i in range(len(data)): 
            #     key=keys[i]
            #     print(key)
            #     value=data[key]
            #     print(value)
            #     pgdb_config={
            #             'host':S_hostIP,
            #             'port':15568,
            #             'user':'CatIsCute',
            #             'password':'raincounter',
            #             'database':'CatIsCute',    }
            #     sqls=(
            #                     """  
            #                     update  public."raincounter_equipment_db"
            #                     set {key} = '{value}'
            #                     WHERE id = '{ID}'
            #                     """.format(
            #                         key=key,
            #                         value=value,
            #                         ID=ID
            #                     )
            #                     )  
            #     conn = psycopg2.connect(**pgdb_config)
            #     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            #     cursor.execute(sqls)    
            #     conn.commit()
            #     conn.close()
            try:
                pgdb_config={
                        'host':S_hostIP,
                        'port':15568,
                        'user':'CatIsCute',
                        'password':'raincounter',
                        'database':'CatIsCute',    }
                sqls=(
                                """  
                                select status from  public."raincounter_equipment_db"                            
                                WHERE id = '{ID}'
                                """.format(
                                    ID=ID
                                )
                                )
                conn = psycopg2.connect(**pgdb_config)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(sqls)   
                result = cursor.fetchall()[0][0]
                print(ID)
                print(result)
                if result=='unregister':
                    pgdb_config={
                        'host':S_hostIP,
                        'port':15568,
                        'user':'CatIsCute',
                        'password':'raincounter',
                        'database':'CatIsCute',    }
                    sqls=(
                                """  
                                update  public."raincounter_equipment_db"
                                set status = 'working'
                                WHERE id = '{ID}'
                                """.format(      
                                    ID=ID
                                )
                                )  
                    conn = psycopg2.connect(**pgdb_config)
                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                    cursor.execute(sqls)    
                    conn.commit()
                    conn.close()
                    print('device status is updated!')
                print('device status is updated!')
            except:
                print('device is register')            
            return JsonResponse('success', safe=False)
        else:
            return JsonResponse('verify error', safe=False)
    except:
        return JsonResponse('revise error', safe=False)
    
    
@api_view(['GET'])
def get_rain_data_download(request):
    queryparams = request.query_params
    device = queryparams['name']
    print(device)
    print(queryparams)
    if 'start_time' in queryparams.keys():
        start_time = queryparams['start_time']
    else:
        start_time = datetime.strftime(datetime.strptime(datetime.strftime(datetime.now(
        ), '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')-timedelta(hours=72), '%Y-%m-%d %H:%M:%S')

    if 'end_time' in queryparams.keys():
        end_time = queryparams['end_time']
    else:
        end_time = datetime.strftime(datetime.strptime(datetime.strftime(datetime.now(
        ), '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')+timedelta(hours=0), '%Y-%m-%d %H:%M:%S')
    try:
        df = rain_data_action.get_data_from_pgdb(device, start_time, end_time)
        df = rain_data_action.min_raindata_to_hour(df)
        temp=NamedTemporaryFile(suffix='.csv')
        df_download=df.drop(columns=['x','y','device','time','count'])
        df_download=df_download.apply(lambda x: round(x,2)).rename(columns = {"voltage":"voltage(V)",'rainfall':'rainfall(mm/hr)','temp':'temp(degree)'})
        print(temp.name)
        df_download.to_csv(temp.name)
        download_file=open(temp.name,'rb')
        name=rain_data_action.get_device_name(device)
        start=datetime.strftime(df_download.index[0],'%Y-%m-%d %H-%M-%S')
        end=datetime.strftime(df_download.index[-1],'%Y-%m-%d %H-%M-%S')    
        file_name=name+'_'+start+'-'+end+'.csv'
        print(file_name)          
        response =FileResponse(download_file)
        response['Content-Type']='application/octet-stream'
        response['Content-Disposition']='attachment;filename={0}'.format(file_name)
        return response
    except:
        data = 'error!!!'
        return JsonResponse(data, safe=False)
