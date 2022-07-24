from crontab import CronTab
import os

def SetCrontab():
    my_user_cron = CronTab(user=True)
    S_pyFilePath = os.path.join(os.path.split(os.path.realpath(__file__))[0],"Rain-Counter","status_update.py")
    S_logPath = os.path.join(os.path.split(os.path.realpath(__file__))[0],"debug7.log")
    # job = my_user_cron.new(command='/usr/bin/python3 {} crontab run ac10e1995797cdda4d748c2184cef1bd >> {} 2>&1'.format(S_pyFilePath,S_logPath))
    job = my_user_cron.new(command='/usr/bin/python3 {} >> {} 2>&1'.format(S_pyFilePath,S_logPath))
    job.setall('* * * * *')
    job.set_comment("raincounter server crontab")
    my_user_cron.write() 

if __name__=='__main__':
    SetCrontab()