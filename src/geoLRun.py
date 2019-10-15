#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        geoLRun.py
#
# Purpose:     This function is used to convert a url to the IP address then 
#              find the GPS position of the IP address and draw it on the map.
#
# Author:      Yuancheng Liu
#
# Created:     2019/10/14
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------

import os, sys
import time
import math
import socket
import urllib.request
from urllib.request import urlopen
from json import load
from PIL import Image, ImageDraw

import wx  # use wx to build the UI.
import webbrowser

import geoLGobal as gv
import geoLPanel as gp

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class geoLFrame(wx.Frame):
    """ url/IP gps position finder."""
    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=(1150, 560))
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.SetIcon(wx.Icon(gv.ICO_PATH))
        self.scIPaddr = ''      # url ip address
        self.gpsPos = [0, 0]    # url gps position
        self.SetSizer(self._buidUISizer())

#-----------------------------------------------------------------------------
    def _buidUISizer(self):
        """ Build the main UI Sizer. """
        flagsR = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL
        mSizer = wx.BoxSizer(wx.HORIZONTAL)
        mSizer.AddSpacer(5)
        gv.iMapPanel = self.mapPanel = gp.PanelMap(self)
        mSizer.Add(self.mapPanel, flag=flagsR, border=2)
        mSizer.AddSpacer(5)
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 560),
                                 style=wx.LI_VERTICAL), flag=flagsR, border=2)
        mSizer.AddSpacer(5)
        ctSizer = self._buildCtrlSizer()
        mSizer.Add(ctSizer)
        return mSizer

#-----------------------------------------------------------------------------
    def _buildCtrlSizer(self):
        """ build the control panel sizer. """
        flagsR = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL
        ctSizer = wx.BoxSizer(wx.VERTICAL)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        ctSizer.AddSpacer(5)
        hbox0.Add(wx.StaticText(self, label="Search key:".ljust(20)),
                  flag=flagsR, border=2)
        self.scKeyCB = wx.ComboBox(
            self, -1, choices=['IP', 'URL'], size=(60, 22), style=wx.CB_READONLY)
        self.scKeyCB.SetSelection(0)
        hbox0.Add(self.scKeyCB, flag=flagsR, border=2)
        hbox0.AddSpacer(10)
        hbox0.Add(wx.StaticText(
            self, label="Map ZoomIn Level".ljust(20)), flag=flagsR, border=2)
        self.zoomInCB = wx.ComboBox(
            self, -1, choices=[str(i) for i in range(10, 15)], size=(60, 22), style=wx.CB_READONLY)
        hbox0.Add(self.zoomInCB, flag=flagsR, border=2)
        ctSizer.Add(hbox0, flag=flagsR, border=2)
        ctSizer.AddSpacer(5)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.StaticText(self, label="IP/URL: "), flag=flagsR, border=2)
        self.scValTC = wx.TextCtrl(self, size=(230, 22))
        hbox1.Add(self.scValTC, flag=flagsR, border=2)
        hbox1.AddSpacer(2)
        self.searchBt = wx.Button(self, label='Search', size=(60, 22))
        self.searchBt.Bind(wx.EVT_BUTTON, self.onSearch)
        hbox1.Add(self.searchBt, flag=flagsR, border=2)
        ctSizer.Add(hbox1, flag=flagsR, border=2)
        ctSizer.AddSpacer(5)
        ctSizer.Add(wx.StaticText(self, label="Detail Information"),
                    flag=flagsR, border=2)
        ctSizer.AddSpacer(5)
        self.detailTC = wx.TextCtrl(
            self, size=(330, 300), style=wx.TE_MULTILINE)
        ctSizer.Add(self.detailTC, flag=flagsR, border=2)
        self.searchBt = wx.Button(
            self, label='Mark on google map >>', size=(150, 22))
        self.searchBt.Bind(wx.EVT_BUTTON, self.onMark)
        ctSizer.Add(self.searchBt, flag=flagsR, border=2)
        return ctSizer

#-----------------------------------------------------------------------------
    def onSearch(self, event):
        """ convert a url to the IP address then  find the GPS position of the 
            IP address and draw it on the map.
        """
        val = self.scValTC.GetValue()
        self.updateDetail(val)
        self.scIPaddr = val if self.scKeyCB.GetSelection() == 0 else str(socket.gethostbyname(val))
        self.updateDetail(self.scIPaddr)
        # get the gps pocition: 
        (lat, lon) = self.getGpsPos(self.scIPaddr)
        self.gpsPos = [float(lat), float(lon)]
        pilImg = self.getGoogleMap(float(lat), float(lon), 3, 2, 13)
        bitmap = self.PIL2wx(pilImg)
        self.mapPanel.updateBitmap(bitmap)
        self.mapPanel.updateDisplay()

#-----------------------------------------------------------------------------
    def onMark(self, event):
        """ Creat the google map mark url and open the url by the system default browser.
        """
        url = "http://maps.google.com/maps?z=12&t=m&q=loc:" + \
            str(self.gpsPos[0])+"+"+str(self.gpsPos[1])
        webbrowser.open_new(url)
        webbrowser.get('chrome').open_new(url)

#-----------------------------------------------------------------------------
    def getGpsPos(self, ipaddr):
        """ connect to the https://ipinfo.io to get the input ipaddr's gps popsition
        """
        response = urlopen('https://ipinfo.io/' + str(ipaddr) + '/json')
        data = load(response)
        (lat, lon) = (0, 0)
        for attr in data.keys():

            datastr = str(attr).ljust(13)+data[attr]
            self.updateDetail(datastr)
            if attr == 'loc': (lat, lon) = data[attr].split(',')
        return (lat, lon)

#-----------------------------------------------------------------------------
    def PIL2wx(self, image):
        """ Convert the PIL image to wx bitmap.
        """
        width, height = image.size
        return wx.BitmapFromBuffer(width, height, image.tobytes())

#-----------------------------------------------------------------------------
    def wx2PIL(self, bitmap):
        """ Convert the wxBitmap to PIL image.
        """
        size = tuple(bitmap.GetSize())
        try:
            buf = size[0]*size[1]*3*"\x00"
            bitmap.CopyToBuffer(buf)
        except:
            del buf
            buf = bitmap.ConvertToImage().GetData()
        return Image.frombuffer("RGB", size, buf, "raw", "RGB", 0, 1)

#-----------------------------------------------------------------------------
    def getGoogleMap(self, lat, lng, wTileN, hTileN, zoom):
        """ Download the google map based on the GPS position.
        """
        start_x, start_y = self.getStartTlXY(lat, lng, zoom)
        width, height = 256 * wTileN, 256 * hTileN
        map_img = Image.new('RGB', (width,height))
        for x in range(0, wTileN):
            for y in range(0, hTileN) :
                url = 'https://mt0.google.com/vt?x='+str(start_x+x)+'&y='+str(start_y+y)+'&z='+str(zoom)
                current_tile = str(x)+'-'+str(y)
                urllib.request.urlretrieve(url, current_tile)
                im = Image.open(current_tile)
                map_img.paste(im, (x*256, y*256))              
                os.remove(current_tile)
        return map_img

#-----------------------------------------------------------------------------
    def getStartTlXY(self, lat, lng,zoom):
        """ Generates an X,Y tile coordinate based on the latitude, longitude 
            and zoom level
            Returns:    An X,Y tile coordinate
        """
        tile_size = 256
        # Use a left shift to get the power of 2
        # i.e. a zoom level of 2 will have 2^2 = 4 tiles
        numTiles = 1 << zoom
        # Find the x_point given the longitude
        point_x = (tile_size/ 2 + lng * tile_size / 360.0) * numTiles // tile_size
        # Convert the latitude to radians and take the sine
        sin_y = math.sin(lat * (math.pi / 180.0))
        # Calulate the y coorindate
        point_y = ((tile_size / 2) + 0.5 * math.log((1+sin_y)/(1-sin_y)) * -(tile_size / (2 * math.pi))) * numTiles // tile_size
        return int(point_x), int(point_y)

#-----------------------------------------------------------------------------
    def updateDetail(self, data):
        """ update the data in the detail text field. input 'None' will clear the 
            detail information text field.
        """
        if data is None:
            self.detailTC.Clear()
        else:
            self.detailTC.AppendText(" - %s \n" %str(data))

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        mainFrame = geoLFrame(None, -1, gv.APP_NAME)
        mainFrame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()
