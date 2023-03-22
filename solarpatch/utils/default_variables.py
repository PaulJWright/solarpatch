from datetime import datetime

from matplotlib.colors import ListedColormap

# ...
REQUIRED_KEYS = ["RSUN_OBS", "CDELT1", "CRPIX1", "CRPIX2"]

# Colours and colourmap for plotting
SOLARPATCH_COLORS = ["#FFE9AE", "#A7DBD8", "#ADE4B5", "#72A7B6"]
SOLARPATCH_CMAP = ListedColormap(SOLARPATCH_COLORS, name="solarpatch_cmap")

# JSOC
JSOC_EMAIL = "paul@wrightai.com"
JSOC_DATE_FORMAT = "%Y.%m.%d_%H:%M:%S"
JSOC_BASE_URL = "http://jsoc.stanford.edu/"

# Taken from http://jsoc.stanford.edu/ajax/lookdata.html?ds=hmi.M_720s
# The end_time is not accurate (there is a lag for SHARP patches).
# We cannot use beautifulsoup  as the value is dynamically generated w/ JS.
HMI_DATES = {
    "start_time": datetime(2009, 4, 13, 21, 48, 0),
    "end_time": datetime.now(),
}

# The HMI bitmap dictionary
SHARP_BITMAP_DICT = {
    1: "QUIET",
    2: "ACTIVE",
    33: "ON PATCH & WEAK",
    34: "ON PATCH & ACTIVE",
}

# Taken from http://jsoc.stanford.edu/ajax/lookdata.html?ds=mdi.smarp_96m
MDI_DATES = {
    "start_time": datetime(1996, 4, 23),
    "end_time": datetime(2010, 10, 27, 22, 24, 0),
}

# # The HMI bitmap dictionary
# SMARP_BITMAP_DICT = {
#     1: "QUIET",
#     2: "ACTIVE",s
#     33: "ON PATCH & WEAK",
#     34: "ON PATCH & ACTIVE",
# }

COTEMPORAL_DATE = datetime(2010, 7, 14, 11, 0, 8)
