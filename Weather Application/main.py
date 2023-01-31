import requests                        #To handle API requests
from tkinter import *                  #For the GUI
from PIL import ImageTk, Image         #To display the images
from urllib.request import urlopen     #To open the weather icon image from the URL
from types import SimpleNamespace      #To create dummy objects of JSON data
import json                            #To format received API data
from itertools import groupby          #To group together the forecasted data based on the day into seperate lists
import datetime
from tkintermapview import TkinterMapView  #To display the temperature map


"""
The forecasting function is responsible for displaying the 5-day forcast of a city in tkinter frame2
"""
def forCasting():
    clear_frame([frame2])
    forCasBu.pack_forget()
    #request weather data through API
    weatherDataForecast=requests.get("https://api.openweathermap.org/data/2.5/forecast?q={}&appid=a247d9d1c708df3c1b4a7d12f013bfde&units=metric".format(cityWeth))
    #convert to the data to an JSON object
    weatherForeJ=weatherDataForecast.json()
    forecasts=weatherForeJ["list"]
    FOCAS={}
    for k,v in groupby(forecasts,key=lambda x:x['dt_txt'][:10]):    #group the dictionaries of forecast data into seperate lists based on the date
        FOCAS[k]=list(v)
    forCasLoc=Label(frame2,text="Location: {}, {} ".format(weatherForeJ["city"]["name"],weatherForeJ["city"]["country"]))     #location details label
    forCasLoc.pack()
    """
    Get the min and max temperatures of a day based on the received data
    """
    for k,li in FOCAS.items():
        tempmin=li[0]["main"]["temp_min"]
        tempmax=li[0]["main"]["temp_max"]
        cond=li[0]["weather"][0]["description"]
        condIcoID=li[0]["weather"][0]["icon"]
        for i in range(len(li)):
            if li[i]["main"]["temp_min"]<tempmin:
                tempmin=li[i]["main"]["temp_min"]
            if li[i]["main"]["temp_max"]>tempmax:
                tempmax=li[i]["main"]["temp_max"]
        Day=datetime.datetime.strptime(k,"%Y-%m-%d").strftime('%A')     #convert the date string in the data to a date format
        forCasDa=Label(frame2,text="Day: {}    min= {},   {}   , max= {}".format(Day,tempmin,cond,tempmax))      #label of forecast details for a day
        """
        Next six lines are for getting the weather condition icon details and displaying it through image label
        """
        imageURL="http://openweathermap.org/img/wn/{}@2x.png".format(condIcoID)
        wethIcoOp=Image.open(urlopen(imageURL))
        wethConImg=ImageTk.PhotoImage(wethIcoOp)
        wethIcoLabl=Label(frame2,image=wethConImg,width=50,height=50)
        wethIcoLabl.dontloseit = wethConImg     #this will keep a reference to the icon image
        wethIcoLabl.pack()
        forCasDa.pack()
    """
    Configuring forecast window and hiding the other frames
    """
    currWethBu.pack()
    searchCityBu.pack()
    mapBu.pack()
    frame1.pack_forget()
    frame3.pack_forget()
    frame2.pack(anchor=CENTER)
"""
The Maps function is responsible for showing the temperatture map of the world in tkinter frame 3
"""
def Maps():
    clear_frame([frame3])
    mapBu.forget()
    mapWid=TkinterMapView(frame3,width=800,height=600,corner_radius=0)       #creating a tkinter map object
    mapWid.set_tile_server("https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=a247d9d1c708df3c1b4a7d12f013bfde",max_zoom=22)    #getting map details through API
    mapWid.set_zoom(0)    #setting zoom level to be on a world level
    """
    Configuring map window and hiding the other frames
    """
    mapWid.pack()
    currWethBu.pack()
    forCasBu.pack()
    searchCityBu.pack()
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack(anchor=CENTER)
"""
The currWea function is responsible for displaying the current day's weather condition for a specific city in tkinter frame1
"""
def CurrWea():
    clear_frame([frame1])
    currWethBu.pack_forget()
    #receive current day's weather data through API
    weatherData=requests.get("https://api.openweathermap.org/data/2.5/weather?q={}&appid=a247d9d1c708df3c1b4a7d12f013bfde&units=metric".format(cityWeth))
    todayJ=weatherData.json()      #convert weather data to JSON object
    today=json.dumps(todayJ)        #serilize into JSON format
    today = json.loads(today, object_hook=lambda d: SimpleNamespace(**d))     #create a "dummy" object with the weather data properties
    """
    Next four lines are for getting the weather condition icon details and displaying it through image label
    """
    imageURL="http://openweathermap.org/img/wn/{}@2x.png".format(today.weather[0].icon)
    wethIcoOp=Image.open(urlopen(imageURL))
    wethConImg=ImageTk.PhotoImage(wethIcoOp)
    wethIcoLabl=Label(frame1,image=wethConImg)
    """
    The following lines are for displaying the labels of the weather data
    """
    toLoc=Label(frame1,text=today.name+","+today.sys.country)
    ToCuTemp=Label(frame1,text=today.main.temp)
    toTemps=vars(today.main)
    toCon=Label(frame1,text=today.weather[0].description)
    toVis=Label(frame1,text="Visibility: {}m".format(today.visibility))
    toWind=Label(frame1,text="Wind speed: {}m/s".format(today.wind.speed))
    toLoc.pack()
    ToCuTemp.pack()
    wethIcoLabl.pack()
    wethIcoLabl.dontloseit = wethConImg
    toCon.pack()
    #print remaining weather data other than temperature and location and adding % to humidity values
    for key,value in toTemps.items():
        if key != "temp":
            if key == "humidity":
                toWeh=Label(frame1,text=key+":{}%".format(value))
            else:
                toWeh=Label(frame1,text=key+":{}".format(value))
            toWeh.pack()
    """
    Configuring current weather window and hiding the other frames
    """
    mapBu.pack()
    forCasBu.pack()
    searchCityBu.pack()
    frame2.pack_forget()
    frame3.pack_forget()
    frame1.pack(anchor=CENTER)
"""
The clear_frame function will receive a list of frames and then will delete all of the compponents, except for root which will only forget the items
"""
def clear_frame(frames):
    for frame in frames:
        if frame != root:
            for widgets in frame.winfo_children():
                widgets.destroy()       #delete the components of the frame
        else:
            for widgets in frame.winfo_children():
                widgets.pack_forget()   #hide the components of the root window
"""
The disButtons function is responsible for displaying the list of buttons regularly for the users -- they will be displayed in the root window
"""
def disButtons():
    frame4.pack_forget()
    intoLbl.pack()
    currWethBu.pack()
    forCasBu.pack()
    mapBu.pack()
    searchCityBu.pack()
"""
The submit button is responsible for extracting the user input of the city and then checking if it is actually a city or not
"""
def submit():
    city=cityName.get()
    cityName.set("")
    global cityWeth
    """
    send request to API with the user input as city name to check response (200 or 401) to determine if the city exists
    """
    checkCity=requests.get("https://api.openweathermap.org/data/2.5/weather?q={}&appid=a247d9d1c708df3c1b4a7d12f013bfde".format(city))
    if checkCity.status_code == 200:
        cityWeth=city
        disButtons()
    else:
        invLabel=Label(frame4, text = 'Please enter a valid city.', font=('Arial bold',14))
        invLabel.configure(background="#ADD8E6")
        invLabel.grid(row=2,column=0)
"""
The serach City function is responsible for displaying the home search screen where the user can search for another city
"""
def searchCity():
    cityEntry = Entry(frame4, textvariable= cityName, width=30, font=('Arial', 14), borderwidth=2)
    checkCityBu=Button(frame4,text = 'Submit', font=('Arial bold', 14), command = submit, borderwidth=2)
    cityLabel = Label(frame4, text = 'Please enter a city:', font=('Arial bold', 16), borderwidth=2)
    cityLabel.configure(background="#ADD8E6")
    cityEntry.grid(row=0,column=1)
    cityLabel.grid(row=0,column=0)
    checkCityBu.grid(row=1,column=1, pady=25)
    clear_frame([frame1,frame2,frame3,root])
    startFrame.pack(anchor=CENTER, pady=60)
    frame4.pack(anchor=CENTER, pady=250)

root=Tk()     #Intialize the root windows
root.title("Weather App")
root.configure(background="#ADD8E6")
"""
defining the frames 1,2,3 & 4
"""
''' configured a frame with the Title and logo'''
startFrame = Frame(root)
startFrame.configure(background='#ADD8E6')
startFrame.columnconfigure(0, weight=1)
startFrame.columnconfigure(1, weight=1)

label = Label(startFrame, text="Weather Application", font=('Arial bold', 18))
label.configure(background='#ADD8E6') # setting backround color for this particular widget
label.grid(row=0, column=1, sticky=W+E)

imageBox = Text(startFrame, width=8, height=4)

logo = Image.open("logo.png")
resized_logo = logo.resize((70, 70), Image.ANTIALIAS)
new_logo = ImageTk.PhotoImage(resized_logo)

imageBox.image_create('1.0', image=new_logo)
imageBox.configure(background='black')
imageBox.grid(row=0, column=0, sticky=W+N)

frame1=Frame(root)
frame1=LabelFrame(root, text="Today's Weather", font=('Arial bold', 8), padx=100,pady=30)
frame2=Frame(root)
frame2=LabelFrame(root, text="Weather's Forecast", font=('Arial bold', 8))
frame3=Frame(root)
frame3=LabelFrame(root, text="Temperature Map", font=('Arial bold', 8),padx=100,pady=100)
frame4=Frame(root)
frame4.configure(background="#ADD8E6")
root.geometry("1920x1080")      #Window size
cityName=StringVar()           #Initialize global variable that will store the city name
"""
Defining the label and four buttons one for each task
"""
intoLbl=Label(root,text="Please select one of the following:", font=('Arial bold', 16), width="50",pady="20")
intoLbl.configure(background="#ADD8E6")
forCasBu=Button(root,text="5-day Forcast", font=('Arial bold', 12), command=forCasting, width="50")
forCasBu.configure(background="#77D496")
mapBu=Button(root,text="Temperature Map", font=('Arial bold', 12), command=Maps, width="50")
mapBu.configure(background="#77D496")
currWethBu=Button(root,text="Today's Weather", font=('Arial bold', 12), command=CurrWea, width="50")
currWethBu.configure(background="#77D496")
searchCityBu=Button(root,text="Search another City", font=('Arial bold', 12), command=searchCity, width="50")
searchCityBu.configure(background="#77D496")
searchCity()    #calling the function for the first page
root.mainloop()   #Create infinite loop waiting for an event by the user
