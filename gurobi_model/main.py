from instance import *
import argparse
from model import *

# parse arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-m', '--model', type=str, help='model type')
args = parser.parse_args()
model = args.model

# read instance
instance = Instance()
instance.readInstance("../data")
print(instance)

runModel(instance)