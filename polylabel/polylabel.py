"""python port of polylabel algorithm found here: https://github.com/mapbox/polylabel"""
from Queue import PriorityQueue
from math import sqrt

SQRT2 = 1.414213562


def polylabel(polygon, precision=1.0):
    """find the 'pole of inaccessibility', the most distance point from the polygon outline"""
    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")
    for pt in polygon:
        min_x = min(min_x, pt[0])
        min_y = min(min_y, pt[1])
        max_x = max(max_x, pt[0])
        max_y = max(max_y, pt[1])

    width = max_x - min_x
    height = max_y - min_y
    cellsize = min(width, height)
    half = cellsize / 2.

    cell_queue = PriorityQueue()

    if cellsize == 0:
        return [min_x, min_y]

    x = min_x
    while x < max_x:
        y = min_y
        while y < max_y:
            cell = Cell(x + half, y + half, half, polygon)
            cell_queue.put((-cell.max, cell))
            y += cellsize
        x += cellsize

    best_cell = get_centroid_cell(polygon)

    bbox_cell = Cell(min_x + width / 2., min_y + height / 2., 0, polygon)
    if bbox_cell.dist > bbox_cell.dist:
        best_cell = bbox_cell

    while not cell_queue.empty():
        _, cell = cell_queue.get()
        # update the best cell if we found a better one
        if cell.dist > best_cell.dist:
            best_cell = cell

        # do not drill down further if there's no chance of a better solution
        if cell.max - best_cell.dist <= precision:
            continue

        # split the cell into four cells
        half = cell.half / 2.
        c1 = Cell(cell.x - half, cell.y - half, half, polygon)
        c2 = Cell(cell.x + half, cell.y - half, half, polygon)
        c3 = Cell(cell.x - half, cell.y + half, half, polygon)
        c4 = Cell(cell.x + half, cell.y + half, half, polygon)
        cell_queue.put((-c1.max, c1))
        cell_queue.put((-c2.max, c2))
        cell_queue.put((-c3.max, c3))
        cell_queue.put((-c4.max, c4))

    return best_cell.x, best_cell.y


class Cell(object):
    """class for holding cell info"""
    def __init__(self, x, y, h, polygon):
        self.x = x
        self.y = y
        self.half = h
        self.dist = point_to_polygon_dist(x, y, polygon)
        self.max = self.dist + self.half * SQRT2


def point_to_polygon_dist(x, y, polygon):
    """point to polygon dist"""
    inside = False
    min_dist_sq = float("inf")

    ring = polygon
    n_pts = len(ring)

    for i, j in zip(range(n_pts), rotate(range(n_pts), 1)):
        pa = polygon[i]
        pb = polygon[j]
        if ((pa[1] > y) != (pb[1] > y)) and (x < (pb[0] - pa[0]) * (y - pa[1]) / (pb[1] - pa[1]) + pa[0]):
            inside = not inside
        min_dist_sq = min(min_dist_sq, get_seg_dist_sq(x, y, pa, pb))

    min_dist = sqrt(min_dist_sq)
    if not inside:
        min_dist *= -1

    return min_dist


def get_centroid_cell(polygon):
    """get the centroid of a cell"""
    area = 0
    x = 0
    y = 0
    n_pts = len(polygon)
    for i, j in zip(range(n_pts), rotate(range(n_pts), 1)):
        pa = polygon[i]
        pb = polygon[j]
        f = pa[0] * pb[1] - pb[0] * pa[1]
        x += (pa[0] + pb[0]) * f
        y += (pa[1] + pb[1]) * f
        area += f * 3
    if area == 0:
        return Cell(polygon[0][0], polygon[0][1], 0, polygon)
    return Cell(x / area, y / area, 0, polygon)


def get_seg_dist_sq(px, py, p1, p2):
    """squared distance from (px, py) to line segment [p1, p2]"""
    x = p1[0]
    y = p1[1]
    dx = p2[0] - x
    dy = p2[1] - y

    if dx != 0 or dy != 0:
        tt = ((px - x) * dx + (py - y) * dy) / (dx * dx + dy * dy)
        if tt > 1:
            x = p2[0]
            y = p2[1]
        elif tt > 0:
            x += dx * tt
            y += dy * tt

    dx = px - x
    dy = py - y

    return dx * dx + dy * dy


def rotate(arr, x):
    """rotate an array by x"""
    return arr[-x:] + arr[:-x]
