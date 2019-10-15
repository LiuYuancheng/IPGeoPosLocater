#-----------------------------------------------------------------------------
# Name:        telloGlobal.py
#
# Purpose:     This module is used as the Local config file to set constants, 
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
print("Current working directory is : %s" %dirpath)
APP_NAME = 'Web GeoLocation Finder'

#------<IMAGES PATH>-------------------------------------------------------------
ICO_PATH = "".join([dirpath, "\\img\\geoIcon.ico"])
BGIMG_PATH = "".join([dirpath, "\\img\\background.jpg"])

#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iMapPanel = None