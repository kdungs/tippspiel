#!/usr/bin/env python

from os import mkdir, path
from PIL import Image
from requests import get
from StringIO import StringIO

BASE = "http://www.bundesliga.de/pics/_2012/wappen"
SIZES = (25, 80)
TEAMS = {
    'BVB': 18,
    'BRE': 11,
    'BMG': 17,
    'HOF': 3084,
    'SCF': 33,
    'M05': 36,
    'FCA': 267,
    'F95': 27,
    'HSV': 13,
    'FCN': 22,
    'SGF': 1649,
    'FCB': 10,
    'FFM': 12,
    'B04': 16,
    'VFB': 14,
    'WOB': 56,
    'H96': 44,
    'S04': 24
}

for size in SIZES:
    mkdir("%s" % size)

for t_handle, t_id in TEAMS.items():
    for size in SIZES:
        r = get("%s/%s/%s.png" % (BASE, size, t_id))
        i = Image.open(StringIO(r.content))
        i.save(path.join("%s" % size, "%s.png" % t_handle))
