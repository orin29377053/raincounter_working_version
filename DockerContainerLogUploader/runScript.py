import os
import argparse

def run(ID):
    print("Set containerLogUploader")
    S_pyPath = os.path.join(os.path.split(os.path.realpath(__file__))[0], "containerLogUploader.py")
    os.popen("nohup python3 {} --ID {}&> containerLogUploader_log.out &".format(S_pyPath,ID))
    print("Set containerLogUploader DONE")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ID")
    args = parser.parse_args()
    run(args.ID)