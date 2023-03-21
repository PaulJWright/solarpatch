from matplotlib.colors import ListedColormap

SOLARPATCH_COLORS = ["#FFE9AE", "#A7DBD8", "#ADE4B5", "#72A7B6"]

SOLARPATCH_CMAP = ListedColormap(SOLARPATCH_COLORS, name="solarpatch_cmap")

BASE_URL = "http://jsoc.stanford.edu/"

BITMAP_DICT = {
    1: "QUIET",
    2: "ACTIVE",
    33: "ON PATCH & WEAK",
    34: "ON PATCH & ACTIVE",
}

REQUIRED_KEYS = ["RSUN_OBS", "CDELT1", "CRPIX1", "CRPIX2"]

JSOC_EMAIL = "paul@wrightai.com"
