import argparse


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", required=True, help="Config file location")

    args = vars(ap.parse_args())
    return args
