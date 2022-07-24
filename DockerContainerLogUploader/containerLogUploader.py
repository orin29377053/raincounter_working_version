import os
import datetime
import psycopg2
import psycopg2.extras
import argparse
import time

class dockerContainerLogUploader:
    def __init__(self, S_containerID=None):
        if S_containerID==None:
            S_containerID = os.popen('docker inspect --format="{{.Id}}" raincointer_server').readlines()[0]
        self.S_containerID = S_containerID
        self.lastTime = datetime.datetime.now()
        try:
            S_hostIP = os.getenv('raincounter_db_ip')
            if S_hostIP == None:
                S_hostIP = "34.81.168.56"
        except:
            S_hostIP = "34.81.168.56"
        try:
            self.CI_COMMIT_SHA = os.getenv('CI_COMMIT_SHA')
            if self.CI_COMMIT_SHA == None:
                self.CI_COMMIT_SHA = "Test"
        except:
            self.CI_COMMIT_SHA = "Test"
        self.pgdb_config = {
            'host': S_hostIP,
            'port': '15568',
            'user': 'CatIsCute',
            'password': 'raincounter',
            'database': 'CatIsCute',
        }
        self.go()
    def go(self):
        sqls = """  
            INSERT INTO public."ServerLog"(
                log_content, info_level, "CI_COMMIT_SHA", log_time)
                VALUES ('{S_logContent}', 'container_log', '{CI_COMMIT_SHA}', '{S_logTime}');
            """.format(  
                S_logContent="docker container log scan START!",
                CI_COMMIT_SHA=self.CI_COMMIT_SHA,
                S_logTime=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f"),
            )
        conn = psycopg2.connect(**self.pgdb_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sqls)
        conn.commit()
        conn.close()
        S_NowServerContainerID = os.popen('docker inspect --format="{{.Id}}" raincointer_server').readlines()[0]
        while S_NowServerContainerID == self.S_containerID:
            lastTime_ = datetime.datetime.now()
            L_Logs = os.popen('docker logs raincointer_server -t --since {}'.format(lastTime_.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))).readlines()
            self.lastTime = lastTime_
            for S_logChose in L_Logs:
                sqls = """  
                    INSERT INTO public."ServerLog"(
                        log_content, info_level, "CI_COMMIT_SHA", log_time)
                        VALUES ('{S_logContent}', 'container_log', '{CI_COMMIT_SHA}', '{S_logTime}');
                    """.format(  
                        S_logContent=S_logChose[31:],
                        CI_COMMIT_SHA=self.CI_COMMIT_SHA,
                        S_logTime=S_logChose[:30],
                    )
                conn = psycopg2.connect(**self.pgdb_config)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(sqls)
                conn.commit()
                conn.close()
            time.sleep(1)
        sqls = """  
            INSERT INTO public."ServerLog"(
                log_content, info_level, "CI_COMMIT_SHA", log_time)
                VALUES ('{S_logContent}', 'container_log', '{CI_COMMIT_SHA}', '{S_logTime}');
            """.format(  
                S_logContent="docker container log scan END!",
                CI_COMMIT_SHA=self.CI_COMMIT_SHA,
                S_logTime=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f"),
            )
        conn = psycopg2.connect(**self.pgdb_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sqls)
        conn.commit()
        conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ID")
    args = parser.parse_args()
    dockerContainerLogUploader(args.ID)

