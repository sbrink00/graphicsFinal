import subprocess

font = "timesnewroman/"

def genLines(file):
  with open(file, "r") as f:
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
      #print(len(lines[i]))
      color = []
      color.append(int(lines[i][x]))
      color.append(int(lines[i][x + 1]))
      color.append(int(lines[i][x + 2]))
      temp.append(color)
    lines[i] = temp
  return lines

def writePPM(lines, output):
  width = len(lines[0])
  for i in range(len(lines)):
    line = lines[i]
    for x in range(len(line)):
      line[x] = " ".join([str(y) for y in line[x]])
    line = " ".join(line).strip() + "\n"
    lines[i] = line
  lines.insert(0, "P3\n")
  lines.insert(1, str(width) + " " + str(len(lines) - 1) + "\n")
  lines.insert(2, "255\n")
  with open(font + output + ".ppm", "w") as f:
    f.writelines(lines)

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
  lines,boundaries = divide(font + file)
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
    writePPM(dict[letter], letter)
    genLetterLines(letter)

def removeshading(file):
  black = [0] * 3
  white = [255] * 3
  lines = readPPM(font + file)
  for i in range(len(lines)):
    for x in range(len(lines[i])):
      if not whitepixel(lines[i][x]): lines[i][x] = black
  writePPM(lines, "a")

def genLetterLines(letter):
  output = []
  lines = readPPM(font + letter + ".ppm")
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
  for i in range(len(output)):
    output[i] = " ".join([str(p) for p in output[i]]) + "\n"
  with open(font + letter + ".letter", "w") as f: f.writelines(output)

    #with open(letter + ".ppm")
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
  return pixel[0] == pixel[1] == pixel[2] == 255

def blackpixel(pixel):
  return pixel[0] == pixel[1] == pixel[2] == 0
