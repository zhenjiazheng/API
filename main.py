#!/usr/bin/env python

# __author__ = 'zhengandy'
import sys
import os
from argparse import ArgumentParser

sys.path.extend(os.path.dirname(os.path.abspath(__file__)))
# print os.path.dirname(os.path.abspath(__file__))


ap = ArgumentParser(
    # prog = __file__,
    description='api automation test.'
)

ap.add_argument('-F', dest='case_folder', action="store", type=str, nargs='?', default="Projects/JiHe")
ap.add_argument('-N', dest='number', action="store", type=int, nargs='?', default=0)
ap.add_argument('-S', dest='sleep_time', action="store", type=float, nargs='?', default=0)
ap.add_argument('-P', dest='precondition_folder', action="store", type=str, nargs='?', default="")
ap.add_argument('-DB', dest='database', action="store", type=str, nargs='?', default="waiwang")
ap.add_argument('-CL', dest='caselist', action="store", type=str, nargs='?', default="")
args = ap.parse_args()


os.environ.setdefault('CASE_FOLDER', args.case_folder)
os.environ.setdefault('UT_ITEM', str(args.number-1))
os.environ.setdefault('SLEEP_TIME', str(args.sleep_time))
os.environ.setdefault('PRECONDITION_FOLDER', args.precondition_folder)
os.environ.setdefault('DATABASE', args.database)
os.environ.setdefault('CASELIST', args.caselist)

import testRunner
testRunner.main()
