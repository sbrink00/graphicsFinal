# graphicsFinal
repo for final project for graphics

## Members
Sam Brink

## Original Goals

### Features to Add
- A way to add text to images  
- set  
- save coordinate system  
- commands to add more features to the mdl files so you don't have to go into python files to change things:  
    - set default color  
    - possibly a way to vary the default color to make a color gradient  
    - set 3dstep  
- More general goal of making my engine faster  

### Features to Add if Time allows
- Incorporation of mesh files


## Final Product Documentation

### Overview

- 2d Letters with 5 fonts.   
- color gradient for background for animation.
- extra commands to make easier to use.
- revised certain parts of engine to make faster.

#### New Commands:
(o) after arguments signals it's optional

-word symbol symbol  
  This command creates a word variable (variable name is first argument)  
  and sets its value to the second argument. This can be used to write a
  single letter, word, or sentence. The second argument must be all lowercase. Due to spaces being used to differentiate arguments, to signify a
  space use capital S. Newline is capital N. The phrase "hello world\nyessir"
  would be written "helloSworldNyessir"

-write symbol number number number symbol(o)
  This command takes the word variable previously created and writes its
  value on the screen. First arg is the word you are writing, 2-4 are xyz
  coordinates for location, and optional fifth is optional font.

-writecentered symbol symbol(o) number(o) number(o) symbol(o)
  This command takes the word variable previously created and writes its
  value on the screen centered at 0 0 0. This is helpful for rotations append scaling as the default writing of a word at 0 0 0 isn't centered.
  First arg is word variable, second is font, third and fourth are the frames
  where you want the word to appear, fifth is name of color variable

-delay number
  Sets the delay for the gif to the argument given (default is 3)

-dcolor symbol
  Sets the default color for the screen to a color variable given as the
  argument

-color symbol number number number
  Very similar to constants command. Creates a color variable and stores it
  in the symbols table. This color can be accessed later for writing letters.
  First argument is color name, 2, 3, and 4 are r, g, and b.

-dcolor_gradient symbol symbol number number
  Creates a gradient in the background color for gifs between the two
  colors (given as the first two arguments) throughout the frames specified
  (given as the last two arguments). Similarly to knobs, if this command is
  used, the background color must be defined for all frames, although you can use multiple commands to achieve this to get more detail.

-step_three_d number
  Sets the 3d step to the argument given (default is 10)




#### Fonts:  
Available fonts are   
-times new roman (written as tnr in mdl files)  
-pinyon  
-comic sans  
-lobster  
-arial  
