#!/usr/bin/python

import numpy
import os, sys
from appJar import gui
import pyserval

targetnode = "7929BCAAA61F80ADD6227E04C477CAB96B5A7EE2BD965A7CC74105830B7C7465"

def pressSetNode(btn):
    pass
    #newsid = app.textBox("Set Node", "Target Node ID")    
    #if newsid != "":
        #targetnode = newsid
        #app.setLabel("lblNode", "bla")
        #print targetnode

def showTplot(btn):
    all_journal = []
    for r in client.rhizome_list()["rows"]:        
        if r[2] == "SENSORLOG" and r[-1] == "temp_csv":
            if r[11] == targetnode:
                print "BID", r[3]
                for l in client.rhizome_get_raw(r[3]).split("\n"):
                    if len(l) > 1:
                        all_journal.append(l.split(" ")[1])

    len_aj = len(all_journal)
    plotlen = min(len_aj, 10)
    x = numpy.arange(0.0, plotlen, 1.0)    
    y = numpy.array(all_journal[len_aj - plotlen : len_aj])

    #x = numpy.arange(0.0, 10.0, 1.0)    
    #y = numpy.array([3, 4, 5, 2, 2, 3, 5, 6, 8, 2])


    app = gui()
    app.setTitle("Temperature Plot")
    axes = app.addPlot("p1", x, y)
    axes.legend(['Temperature in C'])
    app.go()

def showRplot(btn):
    all_journal = []
    for r in client.rhizome_list()["rows"]:        
        if r[2] == "SENSORLOG" and r[-1] == "rad_csv":
            if r[11] == targetnode:
                print "BID", r[3]
                for l in client.rhizome_get_raw(r[3]).split("\n"):
                    if len(l) > 1:
                        all_journal.append(l.split(" ")[1])

    len_aj = len(all_journal)
    plotlen = min(len_aj, 10)
    x = numpy.arange(0.0, plotlen, 1.0)    
    y = numpy.array(all_journal[len_aj - plotlen : len_aj])


    app = gui()
    app.setTitle("Radiation Plot")
    axes = app.addPlot("p1", x, y)
    axes.legend(['Radiation'])
    app.go()

def showGmap(btn):
    coords = []
    for r in client.rhizome_list()["rows"]:        
        if r[2] == "SENSORLOG" and r[-1] == "gps_csv":
            if r[11] == targetnode:
                print "BID", r[3]
                for l in client.rhizome_get_raw(r[3]).split("\n"):
                    if len(l) > 1:
                        entry = l.split(" ")
                        coords.append(entry[1] + "x" + entry[2])
    #app = gui()
    #app.addGoogleMap("m1")
    #app.setGoogleMapSize("m1", "300x500")
    #app.setGoogleMapLocation("m1", "50.816243449867386 8.813151035759148")
    #app.setGoogleMapMarker("m1", "50.816243449867386 8.813151035759148")
    #app.go()
    #coords = ["50.816243449867386x8.813151035759148"]
    print coords
    os.system("python nicermap.py " + " ".join(coords))

def pressDisplay(btn):
    if btn == "Temp":
        print "temp"
        showTplot(None)
    elif btn == "Rad":
        print "rad"
        showRplot(None)
    elif btn == "Pos":
        print "pos"
        showGmap(None)
    else:
        print "unknown button"

client = pyserval.ServalRestClient("pum", "pum123")
for r in client.rhizome_list()["rows"]:
    if r[2] == "SENSORLOG" and r[-1] == "rad_csv":
        if r[11] == targetnode:
            print "BID", r[3]
            print client.rhizome_get_raw(r[3])


app = gui()
app.useTtk()
app.setTitle("NICER Sensors")
app.addImage("nicerlogo","res/nicerlogo.png")
#app.addLabel("title", "Sensor Control")
app.addHorizontalSeparator()
app.addLabel("lblCtrl", "Sensor Control")
app.addLink("Node: ", pressSetNode)
app.addLabel("lblNode", targetnode[0:6] + "*")
app.addCheckBox("Temperature")
app.addCheckBox("Radiation")
app.addCheckBox("GPS Position")
app.addButtons(["Apply" , "Refresh", "Status"], None)
#app.addButton("Status", None)
app.addHorizontalSeparator()
app.addLabel("lblDisplay", "Display Sensors")
app.addButtons(["Temp", "Rad","Pos"], pressDisplay)
#app.setLabelBg("title", "red")

app.go()