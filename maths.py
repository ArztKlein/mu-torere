import math

def dist(x1, y1, x2, y2):
    xlen = x2 - x1
    ylen = y2 - y1

    return math.sqrt(xlen**2 + ylen**2)