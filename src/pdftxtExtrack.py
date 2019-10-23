#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        geoLRun.py
#
# Purpose:     This module is used PyPDF to convert a url to the IP address then 
#              find the GPS position it and draw it on the google map.
#              link: https://www.geeksforgeeks.org/working-with-pdf-files-in-python/
#
# Author:      Yuancheng Liu
#
# Created:     2019/10/14
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------

# importing required modules 
import PyPDF2 
  
# creating a pdf file object 
pdfFileObj = open('../doc/AmazonAtlas_v1.pdf', 'rb') 
  
# creating a pdf reader object 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
  
# printing number of pages in pdf file 
print(pdfReader.numPages) 
  
# creating a page object

# Split 
print("Get all server indicate ID:")
servKey = []
for i in range(3):
    pageObj = pdfReader.getPage(i)
    # extracting text from page 
    for line in pageObj.extractText().split('\n'):
        if line and (line[0] == 'o' or line[0] == '*'):
            data = line.split(' ')
            if str(data[2]).isupper():
                servKey.append(data[2])

print(servKey)
# closing the pdf file object 
pdfFileObj.close() 