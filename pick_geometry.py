#!/usr/bin/env python
from __future__ import print_function, division
import sys
import os
import subprocess
import tempfile
from math import floor

if sys.version_info >= (3, 0):
    from tkinter import Tk, Frame, Canvas, NW
else:
    from Tkinter import Tk, Frame, Canvas, NW
from PIL import ImageTk, Image

def is_video_file( fname ):
    """Tries to guess, whether the file is video or not"""
    _, ext = os.path.splitext(fname)
    return ext.lower() in (".mp4",".avi",".mov",".mkv",".ogg",".ogv", ".mpg", ".3gp", ".ogm", ".v8")

def ffmpeg_make_screenshot( video_file, save_as, time=5.0, ffmpeg_executable="ffmpeg" ):
    """Create a screensot of the video, using FFMPEG"""
    #ffmpeg -loglevel error -i $1 -ss 00:00:5.0 -f image2 -vframes 1 ${tmpfile} 
    time_str="%d:%d:%g"%(floor(time/3600), floor(time/60), time % 60)
    args = [ffmpeg_executable,
            "-loglevel", "error", 
            "-i", video_file, 
            "-ss", time_str,
            "-f", "image2",
            "-vframes", "1",
            save_as ]
    try:
        rval = subprocess.call( args )
        if rval != 0:
            raise ValueError("FFMPEG invocation failed")
    except FileNotFoundError:
        print("FFMPEG executable not found")
        raise

class GUI:
    def __init__(self):
        self.point = self.point1 = None
        self.temp_objects=[]
        self.format_str="{x1}:{y1}:{w}:{h}"
        self.output = None
        self.scale = 1.0
        self.exit_code = 0

    def on_mouse(self, e):
        self.point = (e.x, e.y)

    def on_mouseup(self, e):
        self.point1 = (e.x,e.y)
        x1,y1,x2,y2 = self.get_box()
        canvas = self.canvas
        for i in self.temp_objects:
            canvas.delete(i)
        self.temp_objects = tos = []
        tos.append( canvas.create_rectangle(x1,y1,x2,y2,outline="blue") )
        tos.append( canvas.create_rectangle(x1+1,y1+1,x2-1,y2-1,outline="white") )

    def on_cancel(self,e):
        """User cancelled selection"""
        self.exit_code=1
        self.root.quit()

    def get_box(self):
        if self.point is None: raise ValueError("No selection")
        (x1,x2),(y1,y2) = map(sorted, zip(self.point, self.point1))
        return x1,y1,x2,y2

    def format_result(self):
        x1,y1,x2,y2 = (int(x/self.scale) for x in self.get_box())
        return self.format_str.format( x1=x1, y1=y1, x2=x2, y2=y2, 
                                       w=x2-x1, h=y2-y1, 
                                       cx=(x2+x1)//2, cy=(y1+y2)//2)
        
    def has_selection(self):
        return self.point is not None

    def on_ok(self,e):
        if not self.has_selection(): return
        result = self.format_result()
        if self.output:
            with open(self.output, "w") as ofile:
                print(result, file=ofile)
        else:
            print (result)
        self.root.quit()

    def run(self,fname):
        img = Image.open(fname)
        w,h = img.size
        scale = self.scale
        if scale != 1:
            w1 = int(w*scale)
            h1 = int(h*scale)
            img = img.resize((w1,h1))
            w,h = img.size

        self.root = t = Tk()
        t.bind("<Escape>", self.on_cancel)
        t.bind("q", self.on_cancel)
        t.bind("<Return>", self.on_ok)
        t.bind("<Button-2>", self.on_ok)
        t.title("Select Rectangle")

        frame = Frame(t)
        frame.pack()

        self.canvas = canvas = Canvas(frame, bg="black", width=w, height=h, cursor="tcross")
        canvas.bind("<Button-1>", self.on_mouse)
        canvas.bind("<ButtonRelease-1>", self.on_mouseup)
        canvas.pack()

        photoimage = ImageTk.PhotoImage(image=img)
        canvas.create_image(0, 0, anchor=NW, image=photoimage)

        t.mainloop()


def main():
    from optparse import OptionParser
    parser = OptionParser(usage = "%prog [options] IMAGE_FILE\n"
                          "Query user for the rectagular area on the image and print its coordinates.\n"
                          "Select area with mouse then press [Enter] or <Button-2> to select.\n"
                          "To cancel, press [Esc] or [q].\n"
                          "Coordinates of the selected area are written to the output (stdout by default).")

    parser.add_option("-o", "--output", dest="output",
                      help="write answer to the output file instead of STDOUT (default)", metavar="FILE")
    parser.add_option("-t", "--time", dest="time", type=float, default=5.0,
                      help="when video file is given, takes screenshot at this time, in secons.", metavar="SECONDS")
    parser.add_option("-v", "--video", action="store_true", dest="is_video", default=False,
                      help="force treating file as video")
    parser.add_option("", "--ffmpeg", dest="ffmpeg_executable", default="ffmpeg", metavar="PATH",
                      help="Override path to the FFMPEG executable")
    parser.add_option("-f", "--format", dest="format",
                      help="format string. Possible variables: "
                      "{x1},{y1},{x2},{y2}: corner coordinates, "
                      "{w},{h}: box size, "
                      "{cx},{cy}: center coordinates. "
                      "Default is {x1}:{y1}:{w}:{h}", 
                      metavar="FMT")
    parser.add_option("-s", "--scale", dest="scale", default=100.0, type="float",
                      help="scale loaded image, in percents. Default is 100.", metavar="PERCENT")

    (options, args) = parser.parse_args()
    
    if len(args) < 1:
        parser.error("Input file not specified")
    if len(args) > 1:
        parser.error("Too many input files: "+" ".join(args))
    if options.scale <= 0:
        parser.error("Bad scale, must be positive")
    if options.scale > 10000:
        parser.error("Scale too big")
    
    g = GUI()
    if options.output:
        g.output = options.output
    if options.format:
        g.format_str = options.format
    g.scale = options.scale/100.0

    fname = args[0]
    if options.is_video or is_video_file(fname):
        try:
            tempdir=tempfile.mkdtemp("","pg")
            sshot_file = os.path.join(tempdir, "ss.jpg")
            ffmpeg_make_screenshot(fname, sshot_file, options.time, options.ffmpeg_executable)
            try:
                g.run(sshot_file)
            finally:
                os.remove(sshot_file)
        finally:
            os.rmdir(tempdir)
    else:
        g.run(fname)

    exit(g.exit_code)

if __name__=="__main__":
    main()
