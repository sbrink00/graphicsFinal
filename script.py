from __future__ import print_function
from addImage import addTextImage
import sys
import mdl
from display import *
import display
from matrix import *
from draw import *
import subprocess
import time
from pprint import pprint
import math

def dc(ary):
  return [x if type(x) is not list else dc(x) for x in ary]

"""======== first_pass( commands ) ==========
  Checks the commands array for any animation commands
  (frames, basename, vary)
  Should set num_frames and basename if the frames
  or basename commands are present
  If vary is found, but frames is not, the entire
  program should exit.
  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """
def first_pass( commands ):
    animCommands = ["vary", "frames", "basename", "dcolor_gradient"]
    animCommands  = [x for x in commands if x["op"] in animCommands]
    if len(animCommands) == 0: return "pic",1,None
    animKeywords = [x["op"] for x in animCommands]
    if ("vary" in animKeywords or "basename" in animKeywords or "dcolor_gradient" in animKeywords) and "frames" not in animKeywords:
      raise Exception("Animation commands present but number of frames not defined.")
    if ("vary" in animKeywords or "frames" in animKeywords or "dcolor_gradient" in animKeywords) and "basename" not in animKeywords:
      print("No basename was given so basename set to default: 'pic'.")
      basename = "pic"
    if "basename" in animKeywords:
      for command in animCommands:
        if command["op"] == "basename": basename = command["args"][0]
    for command in animCommands:
      if command["op"] == "frames": num_frames = command["args"][0]
    return (basename, int(num_frames), animCommands)

"""======== second_pass( commands ) ==========
  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).
  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.
  Go through the command array, and when you find vary, go
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value.
  ===================="""
def second_pass( commands, num_frames, symbols ):
    varies = [x for x in commands if x["op"] == "vary"]
    frames = [{} for i in range(num_frames)]
    knobs = []
    for command in varies:
      knob_name = command["knob"]
      if knob_name == "dcolor": raise Exception("not a valid name for a knob")
      knobs.append(knob_name)
      start_frame = int(command["args"][0])
      end_frame = int(command["args"][1])
      if end_frame < start_frame:
        raise Exception("End frame is less than start frame")
      start_value = float(command["args"][2])
      end_value = float(command["args"][3])
      for i in range(start_frame, end_frame + 1):
        percent = 1.0 * (i - start_frame) / (end_frame - start_frame)
        val = percent * (end_value - start_value) + start_value
        frames[i][knob_name] = round(val, 4)
    for frame in frames:
      for knob in knobs:
        if knob not in frame:
          raise Exception("Knob "  + knob + " is not defined for all frames.")
    #SAME IDEA EXCEPT FOR THE DEFAULT COLOR
    dcolors = [x for x in commands if x["op"] == "dcolor_gradient"]
    for command in dcolors:
      args = command["args"]
      c0 = symbols[args[0]]
      c1 = symbols[args[1]]
      start_frame = int(command["args"][2])
      end_frame = int(command["args"][3])
      if end_frame < start_frame:
        raise Exception("End frame is less than start frame")
      for i in range(start_frame, end_frame + 1):
        percent = 1.0 * (i - start_frame) / (end_frame - start_frame)
        color = []
        for a,b in zip(c0, c1):
          temp = percent * abs(a - b)
          val = a + temp if a < b else a - temp
          color.append(round(val))
        frames[i]["dcolor"] = color
    if not dcolors:
      temp = None
      for i in commands:
        if i["op"] == "dcolor": temp = symbols[i["args"][0]]
      temp = [0, 0, 0] if temp != None else temp
      for i in range(len(frames)): frames[i]["dcolor"] = temp
    for frame in frames:
      if "dcolor" not in frame:
        raise Exception("default color not defined for all frames.")
    return frames

def removeAnim(commands):
  idx = 0
  while idx < len(commands):
    c = commands[idx]["op"]
    args = commands[idx]["args"]
    if c in ["basename", "frames", "vary", "delay"]:
      del commands[idx]
      idx -= 1
    idx += 1

def oneTimeCommands(commands, symbols, dcolor):
  idx = 0
  while idx < len(commands):
    c = commands[idx]["op"]
    args = commands[idx]["args"]
    if c == "dcolor":
      co = symbols[args[0]]
      dcolor[0],dcolor[1],dcolor[2] = co[0],co[1],co[2]
      del commands[idx]
      idx -= 1
    elif c in ["color", "constants"]:
      del commands[idx]
      idx -= 1
    idx += 1


def run(filename):
    """
    This function runs an mdl script
    """
    global commands,symbols
    p = mdl.parseFile(filename)
    if p:
        (commands, symbols) = p
    else:
        raise Exception("Unable to parse file.")
    basename, num_frames, animCommands = first_pass(commands)
    if animCommands: knobValues = second_pass(animCommands, num_frames, symbols)
    dcolor = [0, 0, 0]
    DEFAULT_FONT = "lobster/"
    oneTimeCommands(commands, symbols, dcolor)
    removeAnim(commands)
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]
    tmp = new_matrix()
    ident( tmp )
    stack = [ [x[:] for x in tmp] ]
    #for when there are multiple coordinate systems
    stacks = []
    stacks.append(stack)
    screen = new_screen(dcolor)
    zbuffer = new_zbuffer()
    #tmp = []
    step_3d = 10
    delay = 3
    consts = ''
    edges = []
    polygons = []
    words = {}
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    knobCommands = ["move", "rotate", "scale"]
    threeDStuffs = ["box", "sphere", "torus"]
    images = []
    start = time.time()
    for x in range(num_frames):
      print("Now making frame " + str(x), end='\r')
      sys.stdout.flush()
      screen = new_screen(knobValues[x]["dcolor"])
      zbuffer = new_zbuffer()
      stack = [dc(tmp)]
      for i,command in enumerate(commands):
          args = command["args"]
          c = command["op"]
          reflect = ".white"
          if c in knobCommands:
            knob = command["knob"]
            if knob != None:
              val = knobValues[x][knob]
              args = [arg * val if type(arg) in [int, float] else arg for arg in args]
          if c in threeDStuffs:
            const = command["constants"]
            if const != None: reflect = const
            if command["cs"] != None: pass
          if c == "word":
            words[args[0]] = args[1].replace("S", " ").replace( "N", "\n")
          elif c == "write":
            w,xcor,ycor,zcor,size = words[args[0]],int(args[1]),int(args[2]),int(args[3]),int(args[4])
            createWord(xcor, ycor, zcor, w, edges, DEFAULT_FONT, size)
            matrix_mult(stack[-1], edges)
            draw_lines(edges, screen, zbuffer, [100, 100, 255])
            edges.clear()
          elif c == "writecentered":
            w,size = words[args[0]],int(args[1])
            createWordCentered(w, edges, DEFAULT_FONT, size)
            matrix_mult(stack[-1], edges)
            draw_lines(edges, screen, zbuffer, [100, 100, 255])
            edges.clear()
          elif c == "save":
            save_extension(screen, args[0] + ".png")
            print("Filename: " + args[0] + ".png")
            screen.clear()
          elif c ==  "delay":
            delay = int(args[0])
          elif c == "line":
            if command["cs0"] != None: pass
            if command["cs1"] != None: pass
            add_edge( edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult(stack[-1], edges)
            draw_lines(edges, screen, zbuffer, color)
            edges = []
          elif c == "curve": pass
          elif c == "sphere":
            add_sphere(polygons,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult(stack[-1], polygons)
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []
          elif c == "box":
            add_box(polygons,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(stack[-1], polygons)
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []
          elif c == "torus":
            const = command["constants"]
            add_torus(polygons,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), float(args[4]), step_3d)
            matrix_mult(stack[-1], polygons)
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []
          elif c == "pop":
            stack.pop()
          elif c == "push":
            stack.append(dc(stack[-1]))
          elif c == "move":
            if knob != None: pass
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(stack[-1], t)
            stack[-1] = dc(t)
          elif c == "rotate":
            theta = float(args[1]) * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult(stack[-1], t)
            stack[-1] = dc(t)
          elif c == "scale":
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(stack[-1], t)
            stack[-1] = dc(t)
          #it seems like the mdl.py file already does everything I need for constants
          elif c == "constants": pass
          #to be coded later
          elif c == "save_knobs": pass
          elif c == "tween": pass
          elif c == "light": pass
          elif c == "mesh": pass
          elif c == "basename": pass
      fname = basename + str(x) + ".png"
      if num_frames > 1: fname = "anim/" + fname
      images.append(fname)
      #I have not fully implemented the add text image feature
      #so the line below is specific to the gif I am submitting
      #it will be changed and hopefully added to the mdl.py file
      #later.
      #addTextImage(screen, "message.image", (round((XRES - 185) * knobValues[x]["k0"]), 0))
      save_extension(screen, fname)
    if num_frames == 1: return
    termCommand = ["convert", "-delay", str(delay)] + images  + ["movie.gif"]
    subprocess.run(termCommand)
    total = round(time.time() - start)
    m, s = total // 60, total % 60
    print("Time to make gif -  " + str(m) + ":" + str(s))
    print("Gif name: movie.gif")
