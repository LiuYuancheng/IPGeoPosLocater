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
        wx.Panel.__init__(self, parent,  size=(768, 512))
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.bmp =  wx.Bitmap(gv.BGIMG_PATH, wx.BITMAP_TYPE_ANY)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

    def onPaint(self, evt):
        """ Draw the bitmap and the lines."""
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.scale_bitmap(self.bmp, 768, 512), 0, 0)
        dc.SetPen(wx.Pen('RED', width=2, style=wx.PENSTYLE_SOLID))
        l = 8
        dc.DrawLine(384-l, 256, 384+l, 256)
        dc.DrawLine(384, 256-l, 384, 256+l)

    
    def scale_bitmap(self, bitmap, width, height):
        """ resize the bitmap """
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result

    def updateBitmap(self, bitMap):
        self.bmp = bitMap

    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function will 
            set the self update flag.
        """
        self.Refresh(False)
        self.Update()