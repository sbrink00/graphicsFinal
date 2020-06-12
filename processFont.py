import subprocess

font = "lobster/"

def genLines(file):
  with open(font + file, "r") as f:
    lines = f.readlines()
  return lines

def readPPM(file):
  lines = genLines(file)
  info = lines[1].strip().split(" ")
  width = int(info[0])
  height = int(info[1])
  lines = lines[3:]
  lines = [line.strip().split(" ") for line in lines]
  for i in range(height):
    temp = []
    for x in range(0, width * 3, 3):
      color = []
      color.append(int(lines[i][x]))
      color.append(int(lines[i][x + 1]))
      color.append(int(lines[i][x + 2]))
      temp.append(color)
    lines[i] = temp
  return lines

def writePPM(lines, output):
  width = len(lines[0])
  content = lines
  for i in range(len(content)):
    line = content[i]
    for x in range(len(line)):
      line[x] = " ".join([str(y) for y in line[x]])
    line = " ".join(line).strip() + "\n"
    content[i] = line
  content.insert(0, "P3\n")
  content.insert(1, str(width) + " " + str(len(lines) - 1) + "\n")
  content.insert(2, "255\n")
  with open(font + output, "w") as f:
    f.writelines(content)

def divide(file):
  lines = readPPM(file)
  divisions = []
  onspace = True
  start = 0
  end = None
  for i,line in enumerate(lines):
    if onspace and not(whiteline(line)):
      onspace = False
      end = i
      divisions.append([start, end])
    if not onspace and whiteline(line):
      onspace = True
      start = i
  boundaries = []
  for i in range(1, len(divisions)):
    boundary = (divisions[i][1] - divisions[i][0]) // 2 + divisions[i][0]
    boundaries.append(boundary)
  return lines,boundaries

def makeLetters(file):
  lines,boundaries = divide(file)
  alphabet = "abcdefghijklmnopqrstuvwxyz"
  dict = {}
  for i,x in enumerate(alphabet):
    if i == 0: dict[x] = (0, boundaries[0])
    elif i == 25: dict[x] = (boundaries[24], len(lines))
    else: dict[x] = (boundaries[i - 1], boundaries[i])
  for letter in dict:
    s,e = dict[letter]
    dict[letter] = lines[s:e]
  sum = 0
  for letter in dict:
    #removeshading(letter + ".ppm")
    writePPM(dict[letter], letter + ".ppm")
    removeshading(letter + ".ppm")
    genLetterLines(letter)

def removeshading(file):
  black = [0] * 3
  white = [255] * 3
  lines = readPPM(file)
  for i in range(len(lines)):
    for x in range(len(lines[i])):
      if not whitepixel(lines[i][x]):
        #print("reached")
        lines[i][x] = black
  writePPM(lines, file)

def genLetterLines(letter):
  output = []
  lines = readPPM(letter + ".ppm")
  for y in range(len(lines)):
    ml = False
    s = None
    for x in range(len(lines[y])):
      if not ml and blackpixel(lines[y][x]):
        s = x
        ml = True
      if ml and whitepixel(lines[y][x]):
        output.append([s, x - 1, len(lines) - y - 1])
        ml = False
  if font == "tnr/" and letter == "q":
    for i in range(len(output)): output[i] = [int(x * .95) for x in output[i]]
  for i in range(len(output)):
    output[i] = " ".join([str(p) for p in output[i]]) + "\n"
  with open(font + letter + ".letter", "w") as f: f.writelines(output)

def genLetterEdges(letter, z):
  edges = []
  genLetterLines(letter)
  with open(font + letter + ".letter", "r") as f:
    lines = f.readlines()
  lines = [[int(x) for x in y.strip().split(" ")] for y in lines]
  for line in lines:
    edges.append([line[0], line[2], z, 1])
    edges.append([line[1], line[2], z, 1])
  return edges

def whiteline(line):
  for color in line:
    if not (color[0] == color[1] == color[2] == 255): return False
  return True

def whitepixel(pixel):
  return sum(pixel) > 720

def blackpixel(pixel):
  return not whitepixel(pixel)

makeLetters("lobster.ppm")
