#!/bin/sh
#Use pick_grometry to query coordinates of the box in the video frame.
#Requirements:
#  ffmpeg
#  query_geometry.py

tmpdir=`mktemp -d`
tmpfile=${tmpdir}/frame.png
#first save a video frame
ffmpeg -loglevel error -i $1 -ss 00:00:5.0 -f image2 -vframes 1 ${tmpfile} && {
    #then pick a frame
    python pick_geometry.py ${tmpfile}
    rm ${tmpfile}
}

rmdir ${tmpdir}
