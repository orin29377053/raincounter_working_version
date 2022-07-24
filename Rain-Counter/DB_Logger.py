import logging
import psycopg2
import psycopg2.extras
from django.conf import settings
import os
import datetime
import time
import logging
logger = logging.getLogger(__name__)


def INIT_logTable():
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

    S_sqlContent = """
    CREATE TABLE IF NOT EXISTS public."ServerLog"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    log_content text COLLATE pg_catalog."default",
    upload_time timestamp with time zone NOT NULL DEFAULT now(),
    info_level text COLLATE pg_catalog."default",
    "CI_COMMIT_SHA" text COLLATE pg_catalog."default",
    log_time timestamp with time zone,
    CONSTRAINT "ServerLog_pkey" PRIMARY KEY (id, upload_time)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."ServerLog"
    OWNER to "CatIsCute";
    """
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(S_sqlContent)
    conn.commit()
    conn.close()
INIT_logTable()

class RaincounterLoggerHandler(logging.Handler):
    def emit(self, record):
        try:
            S_hostIP = ""
            try:
                S_hostIP = os.getenv('raincounter_db_ip')
            except:
                S_hostIP = ""

            S_CI_COMMIT_SHA = ""
            try:
                S_CI_COMMIT_SHA = os.getenv('CI_COMMIT_SHA')
            except:
                S_CI_COMMIT_SHA = ""


            pgdb_config = {
                'host': S_hostIP,
                'port': '15568',
                'user': 'CatIsCute',
                'password': 'raincounter',
                'database': 'CatIsCute',
            }
            levelname = record.levelname
            message = record.getMessage().replace("'",'"')
            log_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(record.created))
            sqls = (
                """  
                    INSERT INTO "ServerLog" 
                    (log_content, info_level, "CI_COMMIT_SHA", log_time)
                    VALUES 
                    ('{message}', '{levelname}', '{CI_COMMIT_SHA}', '{log_time}') 
                """.format(  
                    message=message,levelname=levelname,CI_COMMIT_SHA=S_CI_COMMIT_SHA,
                    log_time=log_time
                )
            )
            # print(sqls)
            conn = psycopg2.connect(**pgdb_config)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(sqls)
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(e)
            pass