#-----------------------------------------------------------------------------
# Name:        telloGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2019/10/01
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import os

dirpath = os.getcwd()
print("Current working directory is : %s" % dirpath)
APP_NAME = 'Web GeoLocation Finder'

#------<IMAGES PATH>-------------------------------------------------------------
IMG_FD = 'img'
ICO_PATH = os.path.join(dirpath, IMG_FD, "geoIcon.ico")
BGIMG_PATH = os.path.join(dirpath, IMG_FD, "background.jpg")
DC_POS_PATH = os.path.join(dirpath, "awsRecord.txt")

#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iCtrlPanel = None   # panel to do the control
iMapPanel = None    # panel to display the google map.
iGeoMgr = None      # program control manager.
iDCPosMgr = None    # data ceter position manager.