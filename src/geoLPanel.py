#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        TelloPanel.py
#
# Purpose:     This function is used to create the control or display panel for
#              the UAV system.
# Author:      Yuancheng Liu
#
# Created:     2019/10/01
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import wx
import geoLGobal as gv

class PanelMap(wx.Panel):
    """ Map panel to show the google map."""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent,  size=(800, 600))
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.bmp =  wx.Bitmap(gv.BGIMG_PATH, wx.BITMAP_TYPE_ANY)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

    def onPaint(self, evt):
        """ Draw the bitmap and the lines."""
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)
    



