from instance import *
import argparse

# parse arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-m', '--model', type=str, help='model type')
args = parser.parse_args()

model = args.model
