import sys
from display import *
from draw import *
from script import run

view = [0, 0, 1];
ambient = [50, 50, 50]
light = [[0.5, 0.75, 1], [255, 255, 255]]
symbols = {}
symbols['.white'] = ['constants',
                        {'red': [0.2, 0.5, 0.5],
                         'green': [0.2, 0.5, 0.5],
                         'blue': [0.2, 0.5, 0.5]}]

reflect = ".white"
#print(symbols[reflect])
edges = []
black = [0, 0, 0]
red = [255, 0, 0]
screen = new_screen()
zbuffer = new_zbuffer()
polygons = []
#add_box(polygons, 100, 100, 0, 50, 50, 50)
createWord(20, 200, 0, "hello world", edges, "tnr/", size=3)
#createWord(100, 300, 0, "abcdefghijklmn\nopq rstuvwxyz", edges, "tnr/")
#matrix_mult(make_scale(.25, .25, .25), edges)
# matrix_mult(make_rotY(20), polygons)
# matrix_mult(make_translate(200, 600, 0), edges)
draw_lines(edges, screen, zbuffer, red)
#draw_polygons(polygons, screen,  zbuffer, view, ambient, light, symbols, reflect)
save_extension(screen, "pic.png")
