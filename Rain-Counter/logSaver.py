from subprocess import Popen, PIPE
import argparse
import os

S_hostIP = ""
try:
    S_hostIP = os.getenv('raincounter_db_ip')
except:
    S_hostIP = ""

def writeLogToDB(S_logContent):
    print("writeLogToDB")
    print(S_logContent)
    pgdb_config = {
        'host': S_hostIP,
        'port': '15568',
        'user': 'CatIsCute',
        'password': 'raincounter',
        'database': 'CatIsCute',
    }
    print(pgdb_config)


    sqls = (
        """  
            INSERT INTO ServerLog 
            (log_content)
            VALUES 
            ('{S_logContent}') 
        """.format(  
            S_logContent=S_logContent,
        )
    )
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(sqls)
    conn.commit()
    conn.close()

def go(S_command):
    process = Popen([i for i in S_command.split(' ')], stdout=PIPE)
    while True:
        print('test')
        test = process.stdout.readline()
        print('test2')
        if process.poll() != None:
            break
        if test:
            writeLogToDB(test)

if __name__ == '__main__':
    print("testtest")
    parser = argparse.ArgumentParser()
    parser.add_argument("--Command")
    args = parser.parse_args()
    go(args.Command)