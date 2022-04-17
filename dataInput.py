#!/usr/bin/python
'''
Alexander Pushkar
4/11/2021

GUI to interact with the store database
load new information, search for current, or remove

'''

from __future__ import print_function
from ast import Delete, IsNot
from asyncio.base_futures import _FINISHED
from asyncio.windows_events import NULL
from asyncore import write
from cgitb import text
from contextlib import nullcontext
from ctypes import sizeof
from distutils.sysconfig import customize_compiler
from encodings import utf_8, utf_8_sig
from gzip import READ
from itertools import product
from msilib import type_string
from pickle import TRUE
from re import I
from sre_compile import isstring
import this
from tkinter.tix import INTEGER
from turtle import bgcolor, right, title
import unicodedata
from xml.etree.ElementTree import tostring
import mysql.connector
import csv
from tkinter import *  
from tkinter import DISABLED
import tkinter as tk
import random
from mysqlx import Row
from setuptools import Command
import hashlib
import re 
from datetime import date, datetime



#Creates Connection to DB
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "AVR!!20052006",
    database = "customerschema",
    autocommit = True
)





#Creates new screen and titles it
win = tk.Tk(screenName="Data Portal")
win.title("Data Managment Tool")


#Frame to hold seelection Buttons
selectionButtons = Frame(win, bg="#F2D199")
selectionButtons.grid(columnspan=1)


#Frame that output and input options displayed in, seperate frame to ease in deletion
outPutFrame = Frame(win)
outPutFrame.grid(row = 1, column = 1, sticky='news')



#Function to ease creating popup Windows
def popupwin(insert_val):
   #Create a Toplevel window
   top= Toplevel(win, border=4)

   #Create a Button to print something in the Entry widget
   Label(top,text= insert_val).pack(pady= 5,side=TOP)
   #Create a Button Widget in the Toplevel Window
   button= Button(top, text="Ok", command=lambda:top.destroy())
   button.pack(pady=5, side= TOP)


#Function to clear widgets in output windows
def clearOutPutWindow():
    for widget in outPutFrame.winfo_children():
        widget.destroy()

#Creates Date Entry function to ease data entry later in, tk.DateEntry project abondonded. For some reason wont work without Class
class DateEntry(tk.Frame):
    def __init__(self, master, frame_look={}, **look):
        args = dict(relief=tk.SUNKEN, border=1)
        args.update(frame_look)
        tk.Frame.__init__(self, master, **args)

        # arguments to update 
        args = {'relief': tk.FLAT}
        args.update(look)

        #Labels and entry that create layout with arguments
        self.entry_1 = tk.Entry(self, width=2, **args)
        self.label_1 = tk.Label(self, text='/', **args)
        self.entry_2 = tk.Entry(self, width=2, **args)
        self.label_2 = tk.Label(self, text='/', **args)
        self.entry_3 = tk.Entry(self, width=4, **args)

        #Foratming above alables and entries 
        self.entry_1.pack(side=tk.LEFT)
        self.label_1.pack(side=tk.LEFT)
        self.entry_2.pack(side=tk.LEFT)
        self.label_2.pack(side=tk.LEFT)
        self.entry_3.pack(side=tk.LEFT)

        #Used to make accesssing each parameter easier
        self.entries = [self.entry_1, self.entry_2, self.entry_3]

        #To allow program to ensure inputted values dont exceed length and delete if they do on typing them
        self.entry_1.bind('<KeyRelease>', lambda e: self._check(0, 2))
        self.entry_2.bind('<KeyRelease>', lambda e: self._check(1, 2))
        self.entry_3.bind('<KeyRelease>', lambda e: self._check(2, 4))

    #Function removes if values become too long in entry box
    def _backspace(self, entry):
        cont = entry.get()
        entry.delete(0, tk.END)
        entry.insert(0, cont[:-1])

    #Checks if entry excedes its size
    def _check(self, index, size):
        entry = self.entries[index]
        next_index = index + 1
        next_entry = self.entries[next_index] if next_index < len(self.entries) else None
        data = entry.get()

        if len(data) > size or not data.isdigit():
            self._backspace(entry)
        if len(data) >= size and next_entry:
            next_entry.focus()

    def get(self):
        return [e.get() for e in self.entries]










#Below are Button Functions


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def aNCButtonFunc():#function of the button to Add a New Customer
    clearOutPutWindow()
    aNCButtonFrame = Frame(outPutFrame)
    aNCButtonFrame.grid(row = 4, column = 1, pady=10)

    #Creates Label to indicate Name
    Label(aNCButtonFrame, text='Name').grid(row=4, column = 1) 

    #Creates Entry and allignes it with Label above
    nameEntry = Entry(aNCButtonFrame)  
    nameEntry.grid(row=4, column=2) 

    #Function for submitButton
    def submitButtonFunc():

        #Wipes Entry widgit and sets variable 'name' to value in list
        name = nameEntry.get() 
        nameEntry.delete(0, 'end')
        
        #Creates new cursor to wipe its fetchall values
        mycursor = mydb.cursor()

        #Grabs all customers name to ensure entry not already made
        mycursor.execute("SELECT customerName FROM customers")
        outPutName = mycursor.fetchall()


        #Checks name is valid
        if re.search("^[a-zA-Z][a-zA-Z]+ {1}[a-zA-Z]+[a-zA-Z]$" ,name) == None:
            popupwin("Error, Invalid Name\nPlease follow format eg (John Smith))")

        else:
            
            #Splits first and last in string name into list
            nameSplit = name.split(sep = " ")
            #Id is Initals, which grabbing from 0 and 1+index of a space does, then hashes name with current date
            #into unique int of length 5 (With date to allow same name but diff ID)
            id = ("%s%s-%s") % (nameSplit[0][0], nameSplit[1][0], abs(hash(name + (datetime.now()).strftime("%d/%m/%Y %H:%M:%S"))) % (10 ** 5))

            #Inserts values into customers and print success message with uniqe ID
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO customers VALUES (%s, %s)", (id, name))
            popupwin("New Customer %s\nWith Id %s\nAdded To Data Base" % (name, id))
            mycursor.close()
        mycursor.close()
        
        

    #Submit button to add customer to customer table in DB
    submitButton = Button(aNCButtonFrame, text='Submit', command=submitButtonFunc).grid(row=5, column = 2)
   

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-




##DELETE,     Inputs:  Name, Category, Sub Category

def aNPButtonFunc():#function of the button
    clearOutPutWindow()
    aNPButtonFrame = Frame(outPutFrame)
    aNPButtonFrame.grid(row = 4, column = 1, pady=10)

    #Creates Label to indicate Name
    Label(aNPButtonFrame, text='Name').grid(row=4, column = 1) 
    Label(aNPButtonFrame, text='Category').grid(row=6, column = 1)
    Label(aNPButtonFrame, text='Sub Category').grid(row=8, column = 1)


    prodNameEntry = Entry(aNPButtonFrame)
    prodNameEntry.grid(row=4, column = 2)
  

    # Dropdown menu options for category
    categoryOptions = [
        "Furniture",
        "Office Supplies",
        "Technology"
    ]

    #Dropdown menu options for sub-category
    subCategoryOption = [
        "Bookcases",        #-=-=-
        "Chairs",           # Indexs 0-3 = Furniture
        "Furnishings",
        "Tables",           #-=-=-

        "Appliances",       #+|+|+
        "Art",
        "Binders",
        "Envelopes",
        "Fasteners",        # Index 4-12 = Office Supplies
        "Labels",
        "Paper",
        "Storage",
        "Supplies",         #+|+|+

        "Accessories",      #[{}]
        "Copiers",          # Index 13-16 = Technology
        "Machines",
        "Phones",           #[{}]
    ]



    #Will Be Used to update Sub-Category Checkbox to become interactable with specific selections
    #once the category checkbox has a selection made
    subClicked = StringVar()
    subClicked.set( "Select Sub-Category" )

    subSubCategoryOptions = [0]

    subDrop = OptionMenu(aNPButtonFrame , subClicked , *subSubCategoryOptions)
    subDrop.grid(row=8, column=2)
    subDrop.configure(state='disabled')


    #Button for when Category is selected
    def OptionMenu_CheckButton(event):  
        #Actives menu and deletes all values within in
        subDrop.configure(state='active')      
        subClicked.set('')
        subDrop['menu'].delete(0, 'end')

        #By the selection of the category optionmenu sets subSubCategoryOptions to specific values
        if clicked.get() == "Furniture":
            subSubCategoryOptions = subCategoryOption[0:4]
        elif clicked.get() == "Office Supplies":
            subSubCategoryOptions = subCategoryOption[4:12]
        else:
            subSubCategoryOptions = subCategoryOption[13:17]

        #Adds each element in above defined list to subDrop as no way to change entire selection at once
        for choice in subSubCategoryOptions:
            subDrop['menu'].add_command(label=choice, command=tk._setit(subClicked, choice))
        subClicked.set( "Select Sub-Category") 

        pass




    # datatype of menu text
    clicked = StringVar()
    clicked.set( "Select Category" )
    
    drop = OptionMenu(aNPButtonFrame , clicked , *categoryOptions, command = OptionMenu_CheckButton )
    drop.grid(row=6, column=2)



 
    
    

    #Function for submitButton
    def submitButtonFunc():
        prodName = prodNameEntry.get()
        prodNameEntry.delete(0, 'end')
        print(prodName)
        #Creates new cursor to wipe its fetchall values
        mycursor = mydb.cursor()

        #Grabs all customers name to ensure entry not already made
        mycursor.execute("SELECT productID FROM products ORDER BY productID DESC LIMIT 1;")
        maxProdID = mycursor.fetchall()

        #Grabs all customers name to ensure entry not already made
        mycursor.execute("SELECT productName FROM products")
        outPutProducts = mycursor.fetchall()
        
       #Input Validation
        if prodName in outPutProducts:
            popupwin("Error, Name Already In Use")
        elif len(prodName) == 0 or clicked.get()=="Select Category" or subClicked.get()=="Select Sub-Category":
            popupwin("Please Input Values")

        else:
            print(maxProdID[0])
            id = ("%s-%s-%s") % (clicked.get()[0:3].upper(), subClicked.get()[0:2].upper(), int(((maxProdID[0][0])[7:17])) + random.randrange(1,30))
            
            mycursor.execute("INSERT INTO products VALUES (%s, %s, %s, %s)", (prodName, id, clicked.get(), subClicked.get()))
            popupwin(("New Product %s\nWith Id %s,\n%s,%s\nAdded To Data Base" % (prodName, id, clicked.get(), subClicked.get())))
            

            subClicked.set("Select Sub Category")
            subDrop.configure(state='disabled')      
            subDrop['menu'].delete(0, 'end')

            clicked.set("Select Category")

        mycursor.close()

    #Submit button to add customer to customer table in DB
    submitButton = Button(aNPButtonFrame, text='Submit', command=submitButtonFunc).grid(row=10, column = 2)


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-




def aNOLButtonFunc():#function of the button
    clearOutPutWindow()

    #Creates Frame in outPutFrame
    aNOLButtonFrame = Frame(outPutFrame)
    aNOLButtonFrame.grid(row = 4, column = 1, pady=10)

    #Block for productID entry field
    Label(aNOLButtonFrame, text='Product ID:').grid(row=4, column = 1) 
    productIDEntry = Entry(aNOLButtonFrame)
    productIDEntry.grid(row=4, column = 2)

    #Block for customerID entry field
    Label(aNOLButtonFrame, text='Cusomer ID:').grid(row=6, column = 1)
    customerIDEntry = Entry(aNOLButtonFrame)
    customerIDEntry.grid(row=6, column = 2)

    #Filler for GUI
    Label(aNOLButtonFrame, text='').grid(row=7, column = 1)


    #Block for shippingMethod entry field
    selectedShipMethod = StringVar()
    selectedShipMethod.set('Select Shipping')
    shipMethods = ["Standard Class", "Second Class", "First Class"]
    Label(aNOLButtonFrame, text='Shipping:').grid(row=8, column = 1)
    shipMethodEntry = OptionMenu(aNOLButtonFrame, selectedShipMethod, *shipMethods)
    shipMethodEntry.grid(row=8, column = 2)
    
    #Block for segment entry field
    selectedSegment = StringVar()
    selectedSegment.set('Select Segment')
    segments = ["Home Office", "Consumer", "Corporate"]
    Label(aNOLButtonFrame, text='Segment:').grid(row=10, column = 1)
    segmentEntry = OptionMenu(aNOLButtonFrame, selectedSegment, *segments)
    segmentEntry.grid(row=10, column = 2)

    #Block for orderDate entry field
    Label(aNOLButtonFrame, text='Order Date').grid(row=11, column=1)
    orderDate = DateEntry(aNOLButtonFrame)
    orderDate.grid(row = 11, column = 2)

    #Block for shipDate entry field
    Label(aNOLButtonFrame, text='Ship Date').grid(row=12, column=1)
    shipDate = DateEntry(aNOLButtonFrame)
    shipDate.grid(row = 12, column = 2)

    #Filler for GUI
    Label(aNOLButtonFrame, text='').grid(row=13, column = 1)


    #Block for State Selection
    Label(aNOLButtonFrame, text='State:').grid(row=14, column = 1)
    stateEntry = Entry(aNOLButtonFrame)
    stateEntry.grid(row=14, column = 2)

    #Block for City Selection
    Label(aNOLButtonFrame, text='City:').grid(row=15, column = 1)
    cityEntry = Entry(aNOLButtonFrame)
    cityEntry.grid(row=15, column = 2)
    
    #Block for Region Selection
    selectedRegion = StringVar()
    selectedRegion.set('Select Region')
    regions = ["North", "South", "West", "East", "Central"]
    Label(aNOLButtonFrame, text='Region:').grid(row=16, column = 1)
    regionEntry = OptionMenu(aNOLButtonFrame, selectedRegion, *regions)
    regionEntry.grid(row=16, column = 2)

    #Block for Zip Selection
    Label(aNOLButtonFrame, text='Zip:').grid(row=18, column = 1)
    zipEntry = Entry(aNOLButtonFrame)
    zipEntry.grid(row=18, column = 2)


    def submitButtonFunc():

        #Helps with validating date
        def isDateValid(widget):
            month = int(widget.get()[0])
            day = int(widget.get()[1])
            year = int(widget.get()[2])
            if 12 >= month >= 1 and 31 >= day >= 1 and (date.today()).year >= year > 1900:
                return True
            else:
                return False

        #Checks if dates are valid
        if not isDateValid(shipDate) or not isDateValid(orderDate):
            popupwin("Please Enter Valid Date")
            return 0
        #Checks if all fields filled in
        if  len(productIDEntry.get()) == 0 or len(customerIDEntry.get()) == 0 or len(zipEntry.get()) == 0 or len(cityEntry.get()) == 0 or len(stateEntry.get()) == 0 or selectedSegment.get() == "Select Segment" or selectedRegion.get() == "Select Region" or selectedShipMethod.get() == "Select Shipping":
            popupwin("Please Fill All Values")
            return 0

        #Creates three arrays for value verification
        mycursor = mydb.cursor()
        mycursor.execute("SELECT productID FROM products")
        productID = [item for t in mycursor.fetchall() for item in t]
        mycursor.execute("SELECT customerID FROM customers")
        customerID = [item for t in mycursor.fetchall() for item in t]
        states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
               'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
               'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
               'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
               'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

        #Block handles Improperly entered values
        errorMessage = ""

        if productIDEntry.get() not in productID:
            errorMessage += "Product ID not found\n"
        if customerIDEntry.get() not in customerID:
            errorMessage += ("Customer ID not found\n")
        if stateEntry.get() not in states:
            errorMessage += ("Enter State As Abbreviation\n")
        if len(errorMessage) != 0:
            popupwin(errorMessage)
            return 0

        
        #Grabs last digits of ID's from orderIDs and sorts to allow to accsses latest value 
        mycursor.execute("SELECT substring(orderID,9,14) FROM orders")
        orderIDList = mycursor.fetchall()
        orderIDList.sort()
        maxOrderID = int(orderIDList[1][0])

        orderID = ("%s-%s-%d" % ((stateEntry.get())[0:2].upper(), orderDate.get()[2], maxOrderID+1))
        
        #Formating here to mySQL compatiable date format for ease of use, (YEAR:MONTH:DATE)
        shipDateFormatted = "%s-%s-%s" % (shipDate.get()[2],shipDate.get()[0],shipDate.get()[1])
        orderDateFormatted = "%s-%s-%s" % (orderDate.get()[2],orderDate.get()[0],orderDate.get()[1])

        inputTuple = (orderID, productIDEntry.get(), customerIDEntry.get(), orderDateFormatted, shipDateFormatted, selectedShipMethod.get(), selectedSegment.get(), "USA", cityEntry.get(), stateEntry.get(), selectedRegion.get(), zipEntry.get())

        mycursor.execute("INSERT INTO orders VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", inputTuple)
        mycursor.close
        popupwin("Following Order Was Added\nOrderID:%s\tProduct ID:%s\tCustomer ID:%s\nOrder Date:%s\tShip Date:%s\tShip Mode:%s\nSegment:%s\tCountry:%s\tCity:%s\nState:%s\tRegion:%s\tPostal Code:%s" % inputTuple)

        #Defaults all values when finsished 
        productIDEntry.delete(0, 'end')
        customerIDEntry.delete(0, 'end')
        selectedShipMethod.set("Select Shipping")
        selectedSegment.set("Select Segment")
        stateEntry.delete(0, 'end')
        cityEntry.delete(0, 'end')
        selectedRegion.set("Select Region")
        zipEntry.delete(0, 'end')


    Button(aNOLButtonFrame, text='Submit', command=submitButtonFunc).grid(row=20, column = 1)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def vCButtonFunc():#function of the button
    clearOutPutWindow()
    vCButtonFrame = Frame(outPutFrame)
    vCButtonFrame.grid(row = 1, column = 2)
    

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM customers")
    outPutRows = mycursor.fetchall()

    totPages = (int(len(outPutRows)/20)+1)

    startValue = []
    startValue.append(0)

    vCPageNumber = Label(vCButtonFrame, text=("Page number: 1 / %d" % totPages))
    vCPageNumber.grid(row = 20, column = 0)
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    def resultOutputerFunc(start, dir):


        #Increments start value of index by either +20 or -20 depending on scrolling and if not end of page
        if dir==1 and startValue[0]<len(outPutRows)-20:
            startValue[0] = (start+20)
        elif dir==-1 and startValue[0]!=0:
            startValue[0] = (start-20)

        #Handels last page to not go out of bounds
        count = 20
        if startValue[0]+20 > len(outPutRows):
            count = len(outPutRows)%20
        #Else needed to reset if go to back page
        else:
            count = 20

        #Prints results into grid.
        rows = []
        for i in range(20):

            cols = []

            for j in range(2):

                e = Entry(vCButtonFrame, relief=GROOVE)
                
                e.grid(row=i, column=j, sticky=NSEW)

                #If end of list, values are overridden with blank space
                if count-i > 0:
                    e.insert(END, "%s" % ((outPutRows[i+startValue[0]])[j]))
                else:
                    e.insert(END, '')

                e['state'] = "readonly"
                cols.append(e)

            rows.append(cols)

        vCPageNumber.config(text= ("Page number: %d / %d" % ((((startValue[0] / 20)+1),  totPages))))

        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


    nextButton = Button(vCButtonFrame, text="Next Page", command = lambda: resultOutputerFunc(int(startValue[0]), 1))
    backButton = Button(vCButtonFrame, text="Previous Page", command= lambda: resultOutputerFunc(int(startValue[0]), -1))
    nextButton.grid(row = 20, column = 2)
    backButton.grid(row = 20, column = 1)
    
    resultOutputerFunc(0, 0)

    mycursor.close()





#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


def vPButtonFunc():#function of the button to view Products
    clearOutPutWindow()
    vPButtonFrame = Frame(outPutFrame)
    vPButtonFrame.grid(row = 1, column = 2)
    

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM products")
    outPutRows = mycursor.fetchall()

    #Gets Total Number of Pages
    totPages = (int(len(outPutRows)/20)+1)

    #Start value list used to allow accsess withen function and outside
    startValue = []
    startValue.append(0)

    #Page number label
    vPPageNumber = Label(vPButtonFrame, text=("Page number: 1 / %d" % totPages))
    vPPageNumber.grid(row = 20, column = 0)


    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    #Displays the result page
    def resultOutputerFunc(start, dir):

        #Checks if trying to progress foward or back one page
        if dir==1 and startValue[0]<len(outPutRows)-20:
            startValue[0] = (start+20)
        elif dir==-1 and startValue[0]!=0:
            startValue[0] = (start-20)

        #Count set by deault to 20 unless the last page where its set to remaining elements
        count = 20
        if startValue[0]+20 > len(outPutRows):
            count = len(outPutRows)%20

        #For every row we want to display, and each column, new entry is created to display
        rows = []
        for i in range(20):

            cols = []

            for j in range(4):

                e = Entry(vPButtonFrame, relief=GROOVE)
                
                e.grid(row=i, column=j, sticky=NSEW)
                if count-i > 0:
                    e.insert(END, "%s" % ((outPutRows[i+startValue[0]])[j]))
                else:
                    e.insert(END, '')
                e['state'] = "readonly"
                cols.append(e)

            rows.append(cols)

        #Page number updated
        vPPageNumber.config(text= ("Page number: %d / %d" % ((((startValue[0] / 20)+1),  totPages))))

        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    #Buttons to move foward one and back one
    nextButton = Button(vPButtonFrame, text="Next Page", command = lambda: resultOutputerFunc(int(startValue[0]), 1))
    backButton = Button(vPButtonFrame, text="Previous Page", command= lambda: resultOutputerFunc(int(startValue[0]), -1))
    nextButton.grid(row = 20, column = 3)
    backButton.grid(row = 20, column = 2)

    #Initilazies first page  
    resultOutputerFunc(0, 0)

    mycursor.close()


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-



def sCButtonFunc(): #Function to search customers
    clearOutPutWindow()
    sCButtonFrame = Frame(outPutFrame)
    sCButtonFrame.grid(row = 1, column = 2)


    Label(sCButtonFrame, text='Customer Name/ID', justify=RIGHT).grid(row=1, column = 1) 
    

    #entry box for names
    ent1 = Entry(sCButtonFrame) 
    ent1.grid(row=1, column=2) 
 
    
    outputLabel = Label(sCButtonFrame, text = '')
    outputLabel.grid(row=5, column = 1)
    def submitButtonFunc():

        

        if ent1.get() == '':
            outputLabel.config(text = "Please enter Value")
            return 0



        val = (ent1.get(), ent1.get())

        mycursor = mydb.cursor()

        #Searches for names that have it either in first or last and any customer ID that matches input ID
        mycursor.execute("SELECT * FROM customers WHERE (customerName LIKE %s || customerID LIKE %s)", val)
        rows = mycursor.fetchall() 

        #checks if actually in DB
        if len(rows)==0:
            
            outputLabel.config(text = "No Results Found")
        else:
            outputLabel.config(text = ("Name: %s\n ID:     %s  " % (rows[0][1], rows[0][0])))

        mycursor.close()
        ent1.delete(0,last=END)

    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    ent3 = Button(sCButtonFrame, text='Submit', command=submitButtonFunc).grid(row=4, column = 2)
    
# -=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-    
    


def sPButtonFunc():
    clearOutPutWindow()
    sPButtonFrame = Frame(outPutFrame)
    sPButtonFrame.grid(row = 1, column = 2)


    Label(sPButtonFrame, text='Product Name/ID', justify=RIGHT).grid(row=1, column = 1) 
    


    ent1 = Entry(sPButtonFrame) 
    ent1.grid(row=1, column=2) 
 
    
    outputLabel = Label(sPButtonFrame, text = '')
    outputLabel.grid(row=5, column = 1)
    
    def submitButtonFunc():
        if ent1.get() == '':
            outputLabel.config(text = "Please enter Value")
            return 0



        val = (ent1.get(), ent1.get())

        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM products WHERE (productName = %s || productID = %s);", val)
        rows = mycursor.fetchall()

        if len(rows)==0:
            
            outputLabel.config(text = "No Results Found")
        else:
            outputLabel.config(text = rows)

        mycursor.close()
        ent1.delete(0,last=END)


    ent3 = Button(sPButtonFrame, text='Submit', command=submitButtonFunc).grid(row=4, column = 2)


def dCButtonFunc():
    clearOutPutWindow()
    dCButtonFrame = Frame(outPutFrame)
    dCButtonFrame.grid(row = 1, column = 1)
    Label(dCButtonFrame, text = "Enter Customer ID To Remove: ").grid(row = 0, column = 0)
    selectedCustomer = Entry(dCButtonFrame)
    selectedCustomer.grid(row = 1, column = 0)

    def submitButtonFunc():
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM customers WHERE customerID='%s';" % selectedCustomer.get())
        try:
            print(selectedCustomer.get())
            
            print("Deleted")
            popupwin("Customer %s deleted from the Database" % selectedCustomer.get())
            print('finished')
        except:
            popupwin("Customer ID not found")
        selectedCustomer.delete(0, END)    
        mycursor.close()
            
    
    Button(dCButtonFrame, text = 'Submit', command = submitButtonFunc).grid(row = 1, column = 1)


def dPButtonFunc():
    popupwin("NOT PROGRAMED YET")

def dOLButtonFunc():
    popupwin("NOT PROGRAMED YET")

selectionLable = tk.Label(win, text="Please Choose a Selection")
selectionButtons = tk.Frame(win, bg='light blue')
aNCButton = tk.Button(selectionButtons, text="Add New Customer", command=aNCButtonFunc)
aNCButton.pack(fill='x')
aNPButton = tk.Button(selectionButtons, text="Add New Product", command = aNPButtonFunc)
aNPButton.pack(fill='x')
aNOLButton = tk.Button(selectionButtons, text="Add New Order Log", command = aNOLButtonFunc)
aNOLButton.pack(fill='x')
vCButton = tk.Button(selectionButtons, text="View Customers", command = vCButtonFunc)
vCButton.pack(fill='x')
vPButton = tk.Button(selectionButtons, text="View Products", command = vPButtonFunc)
vPButton.pack(fill='x')
sCButton = tk.Button(selectionButtons, text="Search Customers", command = sCButtonFunc)
sCButton.pack(fill='x')
sPButton = tk.Button(selectionButtons, text="Search Products", command = sPButtonFunc)
sPButton.pack(fill='x')
dCButton = tk.Button(selectionButtons, text="Remove Customer", command = dCButtonFunc) 
dCButton.pack(fill='x')
dPButton = tk.Button(selectionButtons, text="Remove Product", command = dPButtonFunc) 
dPButton.pack(fill='x')
dOLButton = tk.Button(selectionButtons, text="Remove Customer", command = dOLButtonFunc) 
dOLButton.pack(fill='x')
cButton = tk.Button(selectionButtons, text="Clear Window", command = clearOutPutWindow)
cButton.pack(fill='x')

selectionLable.grid(row=0, column=0, pady=10)
selectionButtons.grid(row=1, column=0, sticky='news')





win.mainloop()


