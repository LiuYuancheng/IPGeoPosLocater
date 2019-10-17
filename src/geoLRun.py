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


import geoLGobal as gv
import geoLPanel as gp

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class GeoLFrame(wx.Frame):
    """ url/IP gps position finder."""
    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=(1150, 560))
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.SetIcon(wx.Icon(gv.ICO_PATH))
        gv.iGeoMgr = self.geoMgr = GeoMgr(self)
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
        gv.iCtrlPanel = gp.PanelCtrl(self)
        mSizer.Add(gv.iCtrlPanel)
        return mSizer

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class GeoMgr(object):
    """ Manager module to handle the geo position calculation.
    """
    def __init__(self, parent):
        self.scIPaddr = ''      # url ip address
        self.gpsPos = [0, 0]    # url gps position

#-----------------------------------------------------------------------------
    def checkIPValid(self, ipAddr):
        """ check whether a ip address is a valid one
        """
        try:
            socket.inet_aton(ipAddr)
            return True
        except socket.error:
            return False

#-----------------------------------------------------------------------------
    def getGpsPos(self, ipaddr):
        """ connect to the https://ipinfo.io to get the input ipaddr's gps popsition
            under float decimal format.
        """
        data = load(urlopen('https://ipinfo.io/' + str(ipaddr) + '/json'))
        (lat, lon) = (0, 0)
        for attr in data.keys():
            datastr = str(attr).ljust(13)+data[attr]
            if gv.iCtrlPanel: gv.iCtrlPanel.updateDetail(datastr)
            if attr == 'loc': (lat, lon) = data[attr].split(',')
        return (float(lat), float(lon))

#-----------------------------------------------------------------------------
    def urlToIp(self, url):
        """ convert the URL to ip address"""
        return str(socket.gethostbyname(url))

#-----------------------------------------------------------------------------
    def getGoogleMap(self, lat, lng, wTileN, hTileN, zoom):
        """ Download the google map based on the GPS position.
        """
        start_x, start_y = self.getStartTlXY(lat, lng, zoom)
        width, height = 256 * wTileN, 256 * hTileN
        map_img = Image.new('RGB', (width, height))
        for x in range(0, wTileN):
            for y in range(0, hTileN):
                url = 'https://mt0.google.com/vt?x=' + \
                    str(start_x+x)+'&y='+str(start_y+y)+'&z='+str(zoom)
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
#-----------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        mainFrame = GeoLFrame(None, -1, gv.APP_NAME)
        mainFrame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()
