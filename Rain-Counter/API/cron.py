from re import I
from datetime import datetime, timedelta
import psycopg2
import psycopg2.extras
import requests
import json
import pandas as pd
import time

# S_hostIP = ""
# try:
#     S_hostIP = os.getenv('raincounter_db_ip')
# except:
#     S_hostIP = ""

# def status_update(device,status):
#     pgdb_config={
#                     'host':S_hostIP,
#                     'port':15568,
#                     'user':'CatIsCute',
#                     'password':'raincounter',
#                     'database':'CatIsCute',    }
#     sqls=(
#                 """  
#                 update  public."raincounter_equipment_db"
#                 set status = '{status}'
#                 WHERE device = '{device}'
#                 """.format(      
#                     device=device,
#                     status=status
#                 )                            )  
#     conn = psycopg2.connect(**pgdb_config)
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cursor.execute(sqls)
#     conn.commit()
#     conn.close()
# def status_update_action():
#     print('update_status start!!')

#     try:
#         #catch status    
#         pgdb_config={
#                             'host':S_hostIP,
#                             'port':15568,
#                             'user':'CatIsCute',
#                             'password':'raincounter',
#                             'database':'CatIsCute',    }
#         sqls=(
#                     """  
#                     select device,status,is_delete,last_update,voltage from  public."raincounter_equipment_db"

#                     """                            )
#         conn = psycopg2.connect(**pgdb_config)
#         cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cursor.execute(sqls)
#         result = cursor.fetchall()
#         conn.commit()
#         conn.close()

#         #update status   
#         for i in range(len(result)):    
#             device=result[i][0]
#             status=result[i][1]
#             is_delete=result[i][2]
#             last_update=result[i][3]
#             voltage=result[i][4]
#             time_3h_before=(datetime.now()-timedelta(hours=3))  
            
#             if is_delete==1:
#                 print(device,' is_delete')
#                 pass
#             elif status=='unregister':
#                 print(device,'is  unregister')
#                 pass    
#             elif last_update<time_3h_before:
#                 print(device,'is  error')
#                 status_update(device,'error')  
#             elif voltage<=10:
#                 print(device,'is  low_power')
#                 status_update(device,'low_power')  
#             else:
#                 print(device,'is  working')
#                 status_update(device,'working') 
#         print('update_success!!')
#     except:
#         print('error')