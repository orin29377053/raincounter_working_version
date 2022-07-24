import os
import argparse
import psycopg2
import psycopg2.extras
from API.rain_data_action import update_raincounter_eq,update_time_raincounter_eq,update_raincounter_rain_info,check_eq_is_exist
from datetime import datetime, timedelta
import json
import pandas as pd
import time

S_hostIP = ""
try:
    S_hostIP = os.getenv('raincounter_db_ip')
except:
    S_hostIP = ""

pgdb_config = {
    'host': S_hostIP,
    'port': '15568',
    'user': 'CatIsCute',
    'password': 'raincounter',
    'database': 'CatIsCute',
}

def wirteDataIntoDB(ID, MD5, GMT):
    S_datasPath_go = "./dataGet"
    if ID==None:
        for S_ID_Chose in os.listdir(S_datasPath_go):
            for S_MD5_Chose in os.listdir("{}/{}".format(S_datasPath_go, S_ID_Chose)):
                S_filePath = "{}/{}/{}".format(S_datasPath_go, S_ID_Chose,S_MD5_Chose)
                try:
                    putDataToDB(S_filePath, GMT)
                except Exception as e:
                    print('Fail in file: {}'.format(S_filePath))
                    print('Fail message: {}'.format(str(e)))
                    pass
    elif MD5==None:
        for S_MD5_Chose in os.listdir("{}/{}".format(S_datasPath_go, ID)):
            S_filePath = "{}/{}/{}".format(S_datasPath_go, ID,S_MD5_Chose)
            try:
                putDataToDB(S_filePath, GMT)
            except Exception as e:
                print('Fail in file: {}'.format(S_filePath))
                print('Fail message: {}'.format(str(e)))
                pass
    else:
        S_filePath = "{}/{}/{}.txt".format(S_datasPath_go, ID,MD5)
        try:
            putDataToDB(S_filePath, GMT)
        except Exception as e:
            print('Fail in file: {}'.format(S_filePath))
            print('Fail message: {}'.format(str(e)))
            pass


def putDataToDB(S_filePath, GMT):
    if os.path.exists(S_filePath) == False:
        return False

    with open(S_filePath, 'r') as f:
        S_content = f.read()
    raw_data = S_content.split('|')
    # print(raw_data)

    for dataChose in raw_data:
        if len(dataChose) > 0:
            print(dataChose)
            data = dataChose.split(',')
            device = data[0]
            count = data[1]
            x = data[2]
            y = data[3]
            #022-05-10 05:14:00,11.636680
            count_datetime = datetime.strftime(datetime.strptime(data[4], "%Y-%m-%d %H:%M:%S")-timedelta(hours=int(GMT)), "%Y-%m-%d %H:%M:%S")
            # count_datetime = data[4]
            voltage = data[5]
            update_by = data[6]
            temp = data[7]
            sqls = (
                """  
                        INSERT INTO raindata 
                        (device, count, x, y, count_datetime, voltage, update_by, temp)
                        VALUES 
                        ('{device}', '{count}', '{x}', '{y}', '{count_datetime}','{voltage}','{update_by}','{temp}') 
                    """.format(  # 彥凱偷加temp項目
                    device=device,
                    count=count,
                    x=x,
                    y=y,
                    count_datetime=count_datetime,
                    voltage=voltage,
                    update_by=update_by,
                    temp=temp,
                )
            )
            # print(sqls)
            conn = psycopg2.connect(**pgdb_config)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(sqls)
            conn.commit()
            conn.close()
            try:
                print("start update the rain eq info")
                NowDatatime = datetime.now()
                with open("DEBUG_{}.txt".format(datetime.now().strftime("%Y%m%d-%H%M%S")), 'w') as f:
                    pass
                update_raincounter_eq(x, y,voltage, device)
                update_time_raincounter_eq(NowDatatime, device)

                update_raincounter_rain_info(device)
                check_eq_is_exist(device)
                print("all update has complete")

            except:
                print('update_raincounter_rain_info error')

    os.remove(S_filePath)

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ID")
    parser.add_argument("--MD5")
    parser.add_argument("--GMT")
    args = parser.parse_args()
    wirteDataIntoDB(args.ID, args.MD5, args.GMT)