from tkinter import *
from functools import partial
import pandas as pd
from tkinter import *
from tkinter import ttk
from time import strftime
from datetime import datetime
import time
import tkinter.messagebox
import os
import pyrebase
import mysql.connector
import csv
from PIL.ImageTk import PhotoImage
from envVar import firebaseConfig as fc




firebase = pyrebase.initialize_app(fc)
db = firebase.database()


root = Tk()
root.geometry("550x500+600+90")
root.maxsize(550, 500)
root.minsize(550, 500)
root.configure(bg='midnight blue')
root.title("Loan Window")
p1 = PhotoImage(file='[DIGICURE MAIN LOGO].png')
root.iconphoto(FALSE,p1)


name_entry = StringVar()
mob_entry = StringVar()

def back():
    root.destroy()
    import Homepage

def displayLoan():
    root.destroy()
    import LoanTreeView

def new():
    root.destroy()
    import NewLoan


def depo():
    root.destroy()
    import Loan_RepayPage


def export():
    with open('LoanFile.csv', 'w') as file:
        write = csv.writer(file)
        write.writerow(
            ["Name", "Loan Amount", "Interest", "Principal Paid", "Interest Paid", "Principal left", "Interest left",
             "InterestPaidTotal","Date","Last Paid Date" ])
        file.close()
    totalData = db.child('loanData').get()
    for data in totalData.each():
        
        if data.val()['name'] == name_entry.get() or data.val()['mobileNumber'] == (mob_entry.get()):
            with open('LoanFile.csv', 'a') as files:
                # print('Inside this')
                print(mob_entry.get())
                write = csv.writer(files)
                write.writerow([data.val()['name'], data.val()['principalAmount'], data.val()['interestPercent'],
                                data.val()['priciplePaid'], data.val()['principalLeft'], data.val()['interestPaid'],
                                data.val()['interestLeft'], data.val()['interestPaidTillDate'],data.val()['date'], data.val()['lastPaidDate']])
                files.close()
    os.system('LoanFile.csv')


def bal():
    balance = 0
    loanData = db.child('loanData').get()
    try:
        for loan in loanData.each():
            
            if loan.val()['name'] == name_entry.get() and loan.val()['mobileNumber'] == (mob_entry.get()):
                print(f'{name_entry.get()} entered if')
                balData = db.child('mainData').get()
                for var in balData.each():
                    if var.val()['name'] == name_entry.get():
                        balance += int(var.val()['amount'])
                    else:
                        balance += 0
                break
    except:
        tkinter.messagebox.showinfo("Search Mismatch", "No such Name in Directory!!")
    bal_lab = Label(root, bg='midnight blue', fg='gold', width=30, font="Helvetica 12 bold",
                    text="Balance:" + str(balance))
    bal_lab.place(x=10, y=248)
    download = Button(root, text="Download\nBalance Sheet", bg='gold', fg='black', font="Helvetica 11 bold",
                      borderwidth=2, relief=SUNKEN, command=export)
    download.place(x=310, y=235)
    newLoan = Button(root, text="New Loan", bg='gold', fg='black', font="Helvetica 11 bold", borderwidth=2,
                     relief=SUNKEN, command=new)
    newLoan.place(x=120, y=325)
    deposit = Button(root, text="Deposit on Existing Loan", bg='gold', fg='black', font="Helvetica 11 bold",
                     borderwidth=2, relief=SUNKEN, command=depo)
    deposit.place(x=270, y=325)

def sync_up():
    
    totalData = db.child('loanData').get()
    myDataBase = mysql.connector.connect(host="localhost", user="root", passwd="12345",database='ivsLoan')
    mycursor = myDataBase.cursor()
    mycursor.execute('Delete From loanEntry')
    for data in totalData.each():
        dataCollection = 'Insert into loanEntry (name ,mobileNumber ,address ,shopName ,date ,pricipalAmount ,interestPercent ,principlePaid ,interestPaid, principleLeft , interestLeft, InterestPaidTillDate,dateGiven) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        datas = [(data.val()['name'], data.val()['mobileNumber'], data.val()['address'],data.val()['shopName'],data.val()['date'], data.val()['principalAmount'], data.val()['interestPercent'], data.val()['priciplePaid'], data.val()['interestPaid'], data.val()['principalLeft'], data.val()['interestLeft'], data.val()['interestPaidTillDate'],data.val()['lastPaidDate'])]
        mycursor.executemany(dataCollection, datas)
        myDataBase.commit()
    tkinter.messagebox.showinfo('Success', 'Data Synced')
    myDataBase.close()


def sync_down():
    try:
        db.child('loanData').remove()
        myDataBase = mysql.connector.connect(host="localhost", user="root", passwd="12345", database='ivsLoan')
        mycursor = myDataBase.cursor()
        query = 'Select * from loanEntry'
        mycursor.execute(query)
        totalEntries = mycursor.fetchall()
        
        for rows in totalEntries:
            datas = {
                     'name':            rows[0], 'mobileNumber':    rows[1], 'address':               rows[2], 'shopName':     rows[3], 'date': rows[4],
                     'principalAmount': rows[5], 'interestPercent': rows[6], 'priciplePaid':          rows[7], 'interestPaid': rows[8],
                     'principalLeft':   rows[9], 'interestLeft':    rows[10], 'interestPaidTillDate': rows[11], 'lastPaidDate':rows[12]
                    }
            db.child('loanData').push(datas)
        tkinter.messagebox.showinfo('Success', 'Database Synced')
     
    except Exception as e:
        tkinter.messagebox.showerror('Error', e)
    
def updateText(data):
    #update the drop down list
    # Clear the listbox
    my_list.delete(0, END)

    # Add toppings to listbox
    for item in data:
        my_list.insert(END, item)

def fillout(event):
    # Delete whatever is in the entry box
    name.delete(0, END)

    # Add clicked list item to entry box
    name.insert(0, my_list.get(ANCHOR))

def check(event):
    # print("hello")
    # grab what was typed
    typed = name_entry.get()
    print(typed)

    if typed == '':
        data = listVal
    else:
        data = []
        for item in listVal:
            if typed.lower() in item.lower():
                data.append(item)

    # update our listbox with selected items
    updateText(data)


Back = Button(root, text="Back", bg='gold', font="Helvetica 11 bold", borderwidth=4, relief=RAISED, command=back)
Back.place(x=20, y=50)

top_frame = Frame(root, bg='gold', borderwidth=10, relief=RAISED, width=500, height=55)
top_frame.pack(side=TOP, fill=X)

heading = Label(top_frame, bg='gold', fg='black', font="Arial 12 bold", text="---Loan Window---")
heading.pack()

name_lab = Label(root, bg='midnight blue', fg='gold', font="Helvetica 12 bold", text="Name:-")
name_lab.place(x=120, y=100)

name = Entry(root, width=27, textvariable=name_entry, borderwidth=5, relief=SUNKEN, font="Helvetica 11 bold")
name.place(x=200, y=98)

my_list = Listbox(root, font =('arial', 13, 'bold'),height = 2, width=25, justify='left')
my_list.place(x = 200, y=133)

listVal = []
def getNameList():
    listVal = []
    listname = db.child('loanData').get()
    for each in listname.each():
        print(each.val()['name'])
        listVal.append(each.val()['name'])

    listVal = list(set(listVal))
    return listVal

listVal = getNameList()

updateText(listVal)

# Create a binding on the listbox onclick
my_list.bind("<<ListboxSelect>>", fillout)

# Create a binding on the entry box
name.bind("<KeyRelease>", check)

mob_lab = Label(root, bg='midnight blue', fg='gold', font="Helvetica 12 bold", text="Mobile No.:-")
mob_lab.place(x=90, y=184)

mob = Entry(root, width=27, textvariable=mob_entry,borderwidth=5, relief=SUNKEN, font="Helvetica 11 bold")
mob.place(x=200, y=183)

Check = Button(root, text="Check", bg='gold', font="Helvetica 11 bold", borderwidth=4, relief=RAISED, command=bal)
Check.place(x=245, y=220)

down_Frame = Frame(root, bg='gold', borderwidth=10, relief=RAISED)
down_Frame.pack(side=BOTTOM,fill=X)
SyncD_button = Button(down_Frame,text="Sync Down",font="Helvetica 12 bold",bg='midnight blue',fg='gold',command = sync_down)
SyncD_button.pack(side=LEFT,padx=100)
SyncU_button = Button(down_Frame,text="Sync Up",font="Helvetica 12 bold",bg='midnight blue',fg='gold',command= sync_up)
SyncU_button.pack(side=LEFT,padx=10)

Display = Button(root, text="DISPLAY", bg='gold', font="Helvetica 11 bold", borderwidth=4, relief=RAISED, command=displayLoan)
Display.place(x=450, y=50)

root.mainloop()
