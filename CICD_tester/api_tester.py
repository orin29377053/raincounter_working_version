import requests
import argparse
import hashlib
import time
import json 
import psycopg2
import psycopg2.extras

def testAllAPIs(S_ip):
    L_failList = []

    result_checkIOTUpdateDataAPI = checkIOTUpdateDataAPI(S_ip)
    if(result_checkIOTUpdateDataAPI):
        L_failList.append(result_checkIOTUpdateDataAPI)

    if len(L_failList) != 0:
        L_failList = ["{}. {}".format(index+1, content) for index,content in enumerate(L_failList)]
        raise BaseException("Test Error:\r\n{}".format(
            "\r\n".join(L_failList)
        ))


def checkIOTUpdateDataAPI(S_ip):
    pgdb_config = {
        'host': S_ip,
        'port': '15568',
        'user': 'CatIsCute',
        'password': 'raincounter',
        'database': 'CatIsCute',
    }

    # 韌體版本 V1.0.1以下的測試項目
    S_serverURL = "http://"+S_ip+":15566/api/data_upload_iot/"
    S_testTxt = ""
    S_testName = "CICD_Tester"
    for i in range(120):
        S_testTxt += S_testName+",0,121.493979,25.058897,2022-04-16 09:05:00,10.120660,"+S_testName+",24.75|"

    m = hashlib.md5()
    m.update(S_testTxt.encode('utf-8'))
    h = m.hexdigest()

    D_dataTest_Header = {
        "Datas": json.dumps({
            'MD5': h,
            'ID': S_testName,
        })
    }
    response = requests.post(S_serverURL, headers=D_dataTest_Header, data=S_testTxt)
    if response.status_code != 200:
        return "API回應:{}".format(response.status_code)

    
    time.sleep(10)
    sqls=(
        """  
        SELECT COUNT(id) FROM public.raindata
        WHERE device = '{device}'
        """.format(      
            device=S_testName,
        )                            
    )  
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(sqls)
    result = cursor.fetchall()[0]
    conn.commit()
    conn.close()
    
    sqls=(
        """  
        DELETE FROM public.raindata
        WHERE device = '{device}'
        """.format(      
            device=S_testName,
        )                            
    )  
    if int(result[0]) >= 120:
        conn = psycopg2.connect(**pgdb_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sqls)
        conn.commit()
        conn.close()
        return ""
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(sqls)
    conn.commit()
    conn.close()
    return "資料庫數量有誤: {}".format(result[0])

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--IP")
    args = parser.parse_args()
    testAllAPIs(args.IP)
