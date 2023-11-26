from bokeh.plotting import curdoc, figure
import random
import time

def update():
    global i
    temp_y = random.random()
    r.data_source.stream({'x': [i], 'y': [temp_y]})
    i += 1

i = 0
p = figure()
r = p.circle([], [])
curdoc().add_root(p)
curdoc().add_periodic_callback(update, 100)