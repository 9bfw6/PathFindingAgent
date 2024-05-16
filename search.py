import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as animation
from searcher import Searcher
from utils import *
from grid import *
from shapely import Polygon


def gen_polygons(worldfilepath):
    polygons = []
    with open(worldfilepath, "r") as f:
        lines = f.readlines()
        lines = [line[:-1] for line in lines]
        for line in lines:
            polygon = []
            pts = line.split(';')
            for pt in pts:
                xy = pt.split(',')
                polygon.append(Point(int(xy[0]), int(xy[1])))
            polygons.append(polygon)
    return polygons


def gen_polygon_objects(polygons):
    polygon_objects = []
    for polygon_points in polygons:
        point_tuples = [(point.x, point.y) for point in polygon_points]
        new_polygon = Polygon(point_tuples)
        polygon_objects.append(new_polygon)
    return polygon_objects


if __name__ == "__main__":
    epolygons = gen_polygons('TestingGrid/world1_enclosures.txt')
    tpolygons = gen_polygons('TestingGrid/world1_turfs.txt')
    #epolygons = gen_polygons('TestingGrid/world2_enclosures.txt')
    #tpolygons = gen_polygons('TestingGrid/world2_turfs.txt')

    enclosures = gen_polygon_objects(epolygons)
    turfs = gen_polygon_objects(tpolygons)

    source = Point(8, 10)
    dest = Point(43, 45)
    searcher = Searcher(source, dest, enclosures, turfs)



    fig, ax = draw_board()
    draw_grids(ax)
    draw_source(ax, source.x, source.y)  # source point
    draw_dest(ax, dest.x, dest.y)  # destination point

    # Draw enclosure polygons
    for polygon in epolygons:
        for p in polygon:
            draw_point(ax, p.x, p.y)
    for polygon in epolygons:
        for i in range(0, len(polygon)):
            draw_line(ax, [polygon[i].x, polygon[(i + 1) % len(polygon)].x],
                      [polygon[i].y, polygon[(i + 1) % len(polygon)].y])

    # Draw turf polygons
    for polygon in tpolygons:
        for p in polygon:
            draw_green_point(ax, p.x, p.y)
    for polygon in tpolygons:
        for i in range(0, len(polygon)):
            draw_green_line(ax, [polygon[i].x, polygon[(i + 1) % len(polygon)].x],
                            [polygon[i].y, polygon[(i + 1) % len(polygon)].y])

    # calculate res_path and print path cost + expanded nodes
    res_path0 = searcher.breadth_first_search()
    res_path1 = searcher.depth_first_search()
    res_path2 = searcher.greedy_best_first_search()
    res_path3 = searcher.a_star_search()
    res_path4 = searcher.uniform_cost_search()
    res_path = searcher.a_star_search()

    # draw grid with path shown 
    for i in range(len(res_path) - 1):
        draw_result_line(ax, [res_path[i].x, res_path[i + 1].x], [res_path[i].y, res_path[i + 1].y])
        plt.pause(0.1)

    plt.show()
