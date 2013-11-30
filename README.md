pick-geometry
=============

CLI program to query user coordinates of a rectangle on a image.

Shows user provided image and allows to select a rectangular area on it.

Usage
-----

pick_geometry.py image.png

Will show a GUI window with an image. Drag mouse to select rectangular area on the image (selection is shown as a blue-white box).

When done, press Enter or middle mosue key (mouse-1). Coordinates of the selected bow will be written to the stdout, in the format: 

  X:Y:WIDTH:HEIGHT

To cancel selection, press Esc or "q". In this case, nothing is printed, and nonzero error code is set.

Options
-------
Options allow to modify program operation.

  -o FILE, --output=FILE
  By default, selection result is written to the stdout. This option allows to override this behavior.

  -f FMT, --format=FMT  

Format string, allowing to override default format. Must be a string, containing one of the following placeholders:
 
 {x1},{y1},{x2},{y2}: Replaced by corner coordinates.
 {w},{h}: Replaced by box size.
 {cx},{cy}: Replaced by the coordinates of the box center.

Default format is "{x1}:{y1}:{w}:{h}".

  -s PERCENT, --scale=PERCENT

 Scale loaded image, in percents. Default is 100. Selection coordinates are returned in the original pixels. I.e. if you set scale to 50 and select 10x10 box, 20x20 will be returned.

Video support:

  -t SECONDS, --time=SECONDS

For video files, specifies time to take a screenshot, in seconds. Floating-point value.

  -v, --video           

Override default vide detection heuristics, forsing treating file as video.

  --ffmpeg=PATH

Override path to the FFMPEG executable



Requirements
------------

* Python 2.7+ or Python 3.
* Pillow (or PIL) - image library for Python.
* Tkinter - standard Python GUI library.
* FFMPEG (optional) - for taking screenshots of video files

Running the program
-------------------

Linux: make the program executable, or run it with Python.
Windows: run it with Python, or write a batch file.

Installation
------------

Not provided yet. Put somewhere in the path.
