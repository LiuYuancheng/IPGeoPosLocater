# IP_GeoLocation_checker
**This project will show the server GPS position and related Geolocation information on the Google map based on the user typed in URL or IPv4 address.**

###### Main UI View

![](https://github.com/LiuYuancheng/IP_GeoLocation_checker/blob/master/doc/mainUI.png)

###### Development env: Python 3.7

###### Additional Lib need: 

1. wxPython 4.0.6 (build UI this lib need to be installed) 

[wxPython]: https://wxpython.org/pages/downloads/index.html:	"wxPython"

```
pip install -U wxPython 
```

2. API to check IPv4 Address GPS/GeoLocation position: https://ipinfo.io/ (no need to install)
3. API to mark the position on Google map.(no need to install)

###### Program execution cmd: 

```
python geoLRun.py
```

------

##### Program Execution Flow 

| This program will follow below steps to mark the server position on the map: |
| ------------------------------------------------------------ |
| Step 1 :  Parse URL to get the Web link. example ( https://pypi.org/project/wxPython/ ==> pypi.org ) |
| Step 2 : Convert web link to IPv4 address.                   |
| Step 3 : Call ipinfo.io API to convert the IP address to Geo-Location information.(GPS lat and lng) |
| Step 4 : Call Google Map API to download map Tiles based on the user’s image size and zoom in level setting. (Create the google map url link with the marked GPS position for user's further check.) |
| Step 5 : Combine all tiles to one map image, mark the server position and show the map in UI. |

------

##### Program Usage Menu

- Run the program:  `python geoLRun.py`

- The program support type in URL or the IP address. Then select the map zoom in level.(default is 13). 

- Copy the URL/IP address in the textField and press the 'Search' button.

- The Geo-Location information will show in the detail information textField.

- Press 'Mark GOS position on google map >> ' button the program will start the system default browser and mark the GPS position on the google map for user to do the further check. 

- Press the 'Clear' button will clear all the textField. 

  ###### This the an example use the program to find the url "http://www.baidu.com" : 

  ![](https://github.com/LiuYuancheng/IP_GeoLocation_checker/blob/master/doc/mainUI.png)

------

