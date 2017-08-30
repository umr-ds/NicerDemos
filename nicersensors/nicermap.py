#!/usr/bin/python

import sys
from appJar import gui



app = gui("Node Position")
app.addGoogleMap("m1")
app.setGoogleMapSize("m1", "300x500")
#app.searchGoogleMap("m1","50.816243449867386 8.813151035759148")

if len(sys.argv) > 1:
    for i in sys.argv[1:]:
        coord = i.replace("x", " ")
        app.setGoogleMapLocation("m1", coord)
        app.setGoogleMapMarker("m1", coord)
app.go()