#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        TelloRun.py
#
# Purpose:     This function is used to create a controller to control the DJI 
#              Tello Drone and connect to the height sensor.
#
# Author:      Yuancheng Liu
#
# Created:     2019/10/14
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------

import sys
import time

import wx  # use wx to build the UI.
import geoLGobal as gv
import geoLPanel as gp

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class geoLFrame(wx.Frame):
    """ DJI tello drone system control hub."""
    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=(1200, 620))
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.SetSizer(self._buidUISizer())

    def _buidUISizer(self):
        """ Build the UI Sizer. """
        flagsR = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL
        mSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mapPanel = gp.PanelMap(self)
        mSizer.Add(self.mapPanel, flag=flagsR, border=2)
        ctSizer = self._buildCtrlSizer()
        mSizer.Add(ctSizer)
        return mSizer

    def _buildCtrlSizer(self):
        flagsR = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL
        ctSizer = wx.BoxSizer(wx.HORIZONTAL)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        hbox0.Add(wx.StaticText(self, label="Search key:".ljust(20)), flag=flagsR, border=2)
        self.scKeyCB = wx.ComboBox(self, -1, choices=['IP', 'URL'],size=(60, 22), style=wx.CB_READONLY)
        hbox0.Add(self.scKeyCB, flag=flagsR, border=2)
        hbox0.AddSpacer(10)
        hbox0.Add(wx.StaticText(self, label="Map ZoomIN Lvl".ljust(20)), flag=flagsR, border=2)
        self.zoomInCB = wx.ComboBox(self, -1, choices=['1','2','3','4'], size=(60, 22), style=wx.CB_READONLY)
        hbox0.Add(self.zoomInCB, flag=flagsR, border=2)
        ctSizer.Add(hbox0, flag=flagsR, border=2)


        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.StaticText(self, label="IP/URL:".ljust(20)), flag=flagsR, border=2)
        self.scValTC = wx.TextCtrl(self)
        hbox1.Add(self.scValTC, flag=flagsR, border=2)
        ctSizer.Add(hbox0, flag=flagsR, border=2)


        return ctSizer








#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        mainFrame = geoLFrame(None, -1, gv.APP_NAME)
        mainFrame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()