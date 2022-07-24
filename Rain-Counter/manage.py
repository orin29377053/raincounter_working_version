#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys



def main():
    ############### 彥凱加的
    # 取代Crontab功能，觸發status_update.py
    ###############
    print("Set loop_status_update")
    S_pyPath = os.path.join(os.path.split(os.path.realpath(__file__))[0], "loop_status_update.py")
    os.popen("nohup python3 {} &> status_update_log.out &".format(S_pyPath))
    print("Set loop_status_update DONE")


    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RainCounter.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
