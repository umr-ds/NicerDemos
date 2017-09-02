#!/usr/bin/python

import numpy
import os, sys
from appJar import gui
import pyserval

targetnode = "7929BCAAA61F80ADD6227E04C477CAB96B5A7EE2BD965A7CC74105830B7C7465"
targetnode = "CFF7493114DF7A9C0A3E07F960E6CF644ECF6AA62EB1787029CD7E130DD2B065"

waiting = False
status = False

laststatus = ""

def checkChat():
    #print mysid, targetnode, client
    global laststatus, waiting, status
    client = pyserval.ServalRestClient("pum", "pum123")
    if waiting:
        print "checking messages"
        msgs = client.meshms_fetch_list_messages(mysid, targetnode)        
        for msg in msgs['rows']:
            if msg[0] == '<' and msg[-3] == False:                
                if msg[6].startswith("STATUS"):
                    laststatus = msg[6]
                    client.meshms_mark_all_read(mysid, targetnode)
                    waiting = False
                    if status:            
                        app.infoBox("Status", laststatus)
                        status = False                                            
                    break
        
        #print laststatus
        

def pressSetNode(btn):
    pass
    #newsid = app.textBox("Set Node", "Target Node ID")    
    #if newsid != "":
        #targetnode = newsid
        #app.setLabel("lblNode", "bla")
        #print targetnode

def showTplot(btn):
    all_journal = []
    client = pyserval.ServalRestClient("pum", "pum123")
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


    #app = gui()
    #app.setTitle("Temperature Plot")
    #axes = app.addPlot("p1", x, y)
    #axes.legend(['Temperature in C'])
    #app.go()
    app.updatePlot("plottemp", x, y)
    taxes.legend(['Temperature in C'])
    taxes.set_xlabel("Last samples")
    taxes.set_ylabel("Degree C")
    app.refreshPlot("plottemp")

    app.showSubWindow("tempview")

def showRplot(btn):
    all_journal = []
    client = pyserval.ServalRestClient("pum", "pum123")
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
    
    app.updatePlot("plotrad", x, y)    
    raxes.legend(['Radiation'])
    raxes.set_xlabel("Last samples")
    raxes.set_ylabel("Clicks Per Minute")
    app.refreshPlot("plotrad")
    app.showSubWindow("radview")


def showGmap(btn):
    coords = []
    client = pyserval.ServalRestClient("pum", "pum123")
    for r in client.rhizome_list()["rows"]:        
        if r[2] == "SENSORLOG" and r[-1] == "gps_csv":
            if r[11] == targetnode:
                print "BID", r[3]
                for l in client.rhizome_get_raw(r[3]).split("\n"):
                    if len(l) > 1:
                        entry = l.split(" ")
                        coords.append(entry[1] + " " + entry[2])
    
    print coords    
    app.setGoogleMapMarker("m1", "")
    for lonlat in coords:
        app.setGoogleMapMarker("m1", lonlat)
    
    try:
        app.setGoogleMapLocation("m1", lonlat)
    except:
        pass

    app.showSubWindow("gmapview")

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

def pressControl(btn):
    global waiting
    global status

    if btn == "Apply":
        print "apply"
        sensorconfig = ""
        if app.getCheckBox("Radiation"):
            sensorconfig += "-r "
        if app.getCheckBox("Temperature"):
            sensorconfig += "-t "
        if app.getCheckBox("GPS Position"):
            sensorconfig += "-g "
        print sensorconfig
        print mysid
        client.meshms_send_message(mysid, targetnode, "SETCONFIG " + sensorconfig)
    elif btn == "Refresh":
        client.meshms_send_message(mysid, targetnode, "GETSTATUS")
        waiting = True
        print "refresh"        
    elif btn == "Status":
        print "status"
        client.meshms_send_message(mysid, targetnode, "GETSTATUS")
        waiting = True
        status = True
    else:
        print "unknown button"

client = pyserval.ServalRestClient("pum", "pum123")
mysid = client.keyring_fetch()['rows'][0][0]
for r in client.rhizome_list()["rows"]:
    if r[2] == "SENSORLOG" and r[-1] == "rad_csv":
        if r[11] == targetnode:
            print "BID", r[3]
            print client.rhizome_get_raw(r[3])

#print mysid
#for conversation in client.meshms_fetch_list_conversations(mysid)['rows']:    
    #if conversation[2] == targetnode and conversation[3] == False:
        #print conversation
xxx = client.meshms_fetch_list_messages(mysid, targetnode)
for yyy in xxx['rows']:
    if yyy[0] == '<' and yyy[-3] == False:
        print yyy[6]

print xxx["header"]
#sys.exit(1)
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
app.addButtons(["Apply" , "Refresh", "Status"], pressControl)
#app.addButton("Status", None)
app.addHorizontalSeparator()
app.addLabel("lblDisplay", "Display Sensors")
app.addButtons(["Temp", "Rad", "Pos"], pressDisplay)
#app.setLabelBg("title", "red")

app.startSubWindow("tempview", modal=True)
x = numpy.arange(0.0, 10.0, 1.0)    
y = numpy.array([3, 4, 5, 2, 2, 3, 5, 6, 8, 2])
app.setTitle("Temperature Plot")
taxes = app.addPlot("plottemp", x, y)
taxes.legend(['Temperature in C'])
taxes.set_xlabel("Last samples")
taxes.set_ylabel("Degree C")
app.stopSubWindow()

app.startSubWindow("radview", modal=True)
x = numpy.arange(0.0, 10.0, 1.0)    
y = numpy.array([3, 4, 5, 2, 2, 3, 5, 6, 8, 2])
app.setTitle("Radiation Plot")
raxes = app.addPlot("plotrad", x, y)
raxes.legend(['Radiation'])
raxes.set_xlabel("Last samples")
raxes.set_ylabel("Clicks Per Minute")
app.stopSubWindow()

app.startSubWindow("gmapview", modal=True)
app.setTitle("GPS Map")
app.addGoogleMap("m1")
app.setGoogleMapSize("m1", "300x500")
app.stopSubWindow()

app.registerEvent(checkChat)
app.setPollTime(1000)
app.go()