'''
This is the Product Management System
Owner: Do Vuong Phuc
Company: Teky Academy
Date: 18/09/2021
Contact: phuc16102001@gmail.com
Please do not copy the source code
'''

from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import simpledialog

currentAccount = None
accountFilePath = "account.dat"
itemFilePath = "item.dat"
listAccount = []
listItem = []
delimeter = "|"
headingColor = "#003d80"

# ============ Models =====================
class Account:

    username = None
    password = "123456"
    gender = "Male"
    nationality = None
    admin = False
    useCalculator = False
    money = 0

    def __init__(self,username,password,gender,nationality,admin,useCalculator,money=0):
        self.username = username
        if (password!=None):
            self.password = password
        if (gender=="Female"):
            self.gender = gender
        self.nationality = nationality
        if (admin==True):
            self.admin = admin
        if (useCalculator==True):
            self.useCalculator = useCalculator
        if (money>=0):
            self.money = money

    @staticmethod
    def fromString(stringConstruction):
        params = stringConstruction.split(delimeter)
        for i in range(4,6):
            if (params[i]=="True"):
                params[i] = True
            else:
                params[i] = False
        params[-1] = int(params[-1])
        return Account(params[0],params[1],params[2],params[3],params[4],params[5],params[6])

    def __str__(self):
        return ("%s|%s|%s|%s|%s|%s|%d")%(self.username,self.password,self.gender,self.nationality,str(self.admin),str(self.useCalculator),self.money) 

class Item:
    name = "Unknown"
    price = 0

    def __init__(self,name,price):
        self.name = name
        if (price>=0):
            self.price = price

    def __str__(self):
        return ("%s|%d")%(self.name,self.price)

    @staticmethod
    def fromString(stringConstruction):
        params = stringConstruction.split(delimeter)
        params[1] = int(params[1])
        return Item(params[0],params[1])

class Cart:
    listItem = []

    def __init__(self):
        self.listItem.clear()

    def add(self,item,amount):
        dataSet = (item,amount)
        self.listItem.append(dataSet)

    def clear(self):
        self.listItem.clear()

    def total(self):
        totalPrice = 0
        for dataSet in self.listItem:
            item = dataSet[0]
            amount = dataSet[1]
            totalPrice += item.price*amount
        return totalPrice

    def __str__(self):
        space = 10
        s = "Your cart:\n"
        s+= "%s\t%s\t%s\n"%("Name","Amount","Price")
        for dataSet in self.listItem:
            item = dataSet[0]
            amount = dataSet[1]
            s+="%s\t%d\t%d\n"%(item.name,amount,item.price)
        s+="Total: %d$"%(self.total())
        return s

# ============ Utils ======================
def openLogin(win):
    win.destroy()
    loginScreen()

def openMenu(win):
    win.destroy()
    menuScreen()

def openSignup(win):
    win.destroy()
    signupScreen()

def openCreateItem(win):
    win.destroy()
    createItemScreen()

def openDeleteItem(win):
    win.destroy()
    deleteItemScreen()

def openBillingSystem(win):
    win.destroy()
    billingScreen()
    
def loadAccountList(path):
    try:
        listAccount.clear()
        file = open(path,"r")
        dat = file.readlines()
        for line in dat:
            try:
                listAccount.append(Account.fromString(line))
            except:
                pass
        file.close()
    except:
        pass

def loadItemList(path):
    try:
        listItem.clear()
        file = open(path,"r")
        dat = file.readlines()
        for line in dat:
            try:
                listItem.append(Item.fromString(line))
            except:
                pass
        file.close()
    except:
        pass

def appendFile(path,line):
    file = open(path,'a')
    file.write(line+"\n")
    file.close()

def clearSpecial(s):
    special = " ~!@#$%^&*()|.,;'`"
    for c in special:
        s = s.replace(c,'')
    return s

def checkExistAccount(username):
    for account in listAccount:
        if (account.username == username):
            return account
    return None

def checkExistItem(itemName):
    for item in listItem:
        if (item.name==itemName):
            return item
    return None

def writeListItem(path):
    file = open(path,'w')
    for item in listItem:
        file.write(str(item)+'\n')
    file.close()

def writeListAccount(path):
    file = open(path,'w')
    for account in listAccount:
        file.write(str(account)+'\n')
    file.close()

# ============ Login ======================
def showHelp():
    s = "[Help 1]\n"
    s+= "This is the product management system\n"
    s+= "You can store your items' data and create billing\n"
    s+= "To use this application, you need an account\n"
    messagebox.showinfo("Help",s)

    s = "[Help 2]\n"
    s+= "You can signup if you didn't have the account\n"
    s+= "While signing up, you can choose whether the account is admin\n"
    s+= "And whether you want to use the calculator\n"
    messagebox.showinfo("Help",s)
    
    s = "[Help 3]\n"
    s+= "For the admin account, you can create or delete an item\n"
    s+= "For all kind of account, you can create a bill using billing system\n"
    s+= "After created the bill, you need to type the money that customer paid\n"
    s+= "The system will notify the charge\n"
    s+= "And your account will updated the money storage\n"
    messagebox.showinfo("Help",s)

    s = "[Help 4]\n"
    s+= "You can view your information and the money storage\n"
    messagebox.showinfo("Help",s)

def showAboutMe():
    s = "Product management\n"
    s+= "Owner: Do Vuong Phuc\n"
    s+= "Email: phuc16102001@gmail.com\n"
    s+= "Phone number: +84 707 953 475"
    messagebox.showinfo("Information",s)

def showVersion():
    messagebox.showinfo("Information","Version: 1.0")
    
def clickLogin(win,entUsername,entPassword):
    global currentAccount

    loadAccountList(accountFilePath)
    username = clearSpecial(entUsername.get())
    password = clearSpecial(entPassword.get())
    currentAccount = checkExistAccount(username)
    if (currentAccount!=None and currentAccount.password==password):
        openMenu(win)
    else:
        currentAccount = None
        messagebox.showerror("Login","Your account is not correct")

def loginScreen():
    win = Tk()
    win.title("Product management")
    win.geometry("300x300")

    mainMenu = Menu(win)
    helpMenu = Menu(mainMenu,tearoff=0)

    win.configure(menu=mainMenu)
    mainMenu.add_cascade(menu=helpMenu,label="Help")

    helpMenu.add_command(label="Version",command=showVersion)
    helpMenu.add_command(label="Help",command=showHelp)
    helpMenu.add_command(label="About me",command=showAboutMe)
    
    logoSize = (90,90)
    img = Image.open("logo.png").resize(logoSize,Image.ANTIALIAS)
    imgTk = ImageTk.PhotoImage(img)
    lbLogo = Label(win,image=imgTk)
    lbLogo.pack()
    
    lbTitle = Label(win,text="Product management",font=("Arial",15),foreground="#003d80")
    lbTitle.pack(padx=5,pady=5)

    lbUsername = Label(win,text="Username")
    lbUsername.pack()

    entUsername = Entry(win,width = 15)
    entUsername.pack()
    
    lbPassword = Label(win,text="Password")
    lbPassword.pack()

    entPassword = Entry(win,width = 15,show="*")
    entPassword.pack()

    frameBtn = Frame(win,width=20)
    frameBtn.pack(padx=5,pady=5)

    btnLogin = Button(frameBtn,width=10,text="Login",command=lambda:clickLogin(win,entUsername,entPassword))
    btnLogin.grid(row=1,column=1)
    
    btnSignup = Button(frameBtn,width=10,text="Sign up",command=lambda:openSignup(win))
    btnSignup.grid(row=1,column=2)

    mainloop()

# ============ Menu =======================
def clickLogout(win):
    global currentAccount
    
    currentAccount = None
    openLogin(win)

def clickShowInformation():
    global currentAccount

    infoString = "Your information\n\n"
    infoString+= "Username: %s\n"
    infoString+= "Password: %s\n"
    infoString+= "Gender: %s\n"
    infoString+= "Nationality: %s\n"
    infoString+= "Is administrator: %s\n"
    infoString+= "Using calculator: %s\n"
    infoString+= "Money: %d$"
    infoString = infoString%(currentAccount.username,currentAccount.password,currentAccount.gender,currentAccount.nationality,str(currentAccount.admin),str(currentAccount.useCalculator),currentAccount.money)

    messagebox.showinfo("User's information",infoString)

def menuScreen():
    global currentAccount

    win = Tk()
    win.title("Product Management")
    
    lbTitle = Label(win,text="Menu",font=("Arial",15),foreground=headingColor)
    lbTitle.pack(padx=5,pady=5)

    
    btnShowInformation = Button(win,width=20,text="Show information",command=lambda:clickShowInformation())
    btnShowInformation.pack()
    
    btnCreateItem = Button(win,width=20,text="Create new item",command=lambda:openCreateItem(win))
    if (currentAccount.admin==True):
        btnCreateItem.pack()
    
    btnDeleteItem = Button(win,width=20,text="Delete an item",command=lambda:openDeleteItem(win))
    if (currentAccount.admin==True):
        btnDeleteItem.pack()

    btnBillingSystem = Button(win,width=20,text="Billing system",command=lambda:openBillingSystem(win))
    btnBillingSystem.pack()

    btnCalculator = Button(win,width=20,text="Calculator",command=lambda:openCalculator(win))
    if (currentAccount.useCalculator==True):
        btnCalculator.pack()

    btnLogout = Button(win,width=20,text="Logout",command=lambda:clickLogout(win))
    btnLogout.pack()

    mainloop()

# ============ Sign up ====================
def clickSignup(win,entUsername,entPassword,varGender,cmbNationality,varAdmin,varCalculator):
    username = clearSpecial(entUsername.get())
    password = clearSpecial(entPassword.get())
    gender = varGender.get()
    nationality = cmbNationality.get()
    admin = varAdmin.get()
    useCalculator = varCalculator.get()
    newAccount = Account(username,password,gender,nationality,admin,useCalculator)

    loadAccountList(accountFilePath)
    if (checkExistAccount(username)!=None):
        messagebox.showerror("Sign up result","Account existed, please try again")
        return None

    verifyString = "Please verify your information\n\n"
    verifyString+= "Username: %s\n"
    verifyString+= "Password: %s\n"
    verifyString+= "Gender: %s\n"
    verifyString+= "Nationality: %s\n"
    verifyString+= "Is administrator: %s\n"
    verifyString+= "Using calculator: %s\n"
    verifyString = verifyString%(username,password,gender,nationality,str(admin),str(useCalculator))

    answer = messagebox.askokcancel("Sign up",verifyString)
    if (answer==True):
        appendFile(accountFilePath,str(newAccount))
        messagebox.showinfo("Sign up result","You have successfully signed up")
        openLogin(win)

def signupScreen():
    win = Tk()
    win.title("Sign up")
    win.geometry("600x200")

    lbTitle = Label(win,text="Sign up",font=("Arial",15),foreground=headingColor)
    lbTitle.place(x=250,y=10)

    lbUsername = Label(win,text="Username:")
    lbUsername.place(x=30,y=40)

    entUsername = Entry(win,width=20)
    entUsername.place(x=100,y=40)

    lbPassword = Label(win,text="Password:")
    lbPassword.place(x=30,y=80)
    
    entPassword = Entry(win,width=20,show="*")
    entPassword.place(x=100,y=80)

    lbGender = Label(win,text="Gender:")
    lbGender.place(x=30,y=120)

    varGender = StringVar()
    varGender.set("Male")
    rdMale = Radiobutton(win,text="Male",value="Male",var=varGender)
    rdFemale = Radiobutton(win,text="Female",value="Female",var=varGender)
    rdMale.place(x=100,y=120)
    rdFemale.place(x=150,y=120)

    lbNationality = Label(win,text="Nationality:")
    lbNationality.place(x=320,y=40)

    lsNationality = ["Vietnamese","Korean","Japanese","American"]
    cmbNationality = Combobox(win,values=lsNationality,state="readonly")
    cmbNationality.current(0)
    cmbNationality.place(x=390,y=40)

    varAdmin = BooleanVar()
    chkAdmin = Checkbutton(win,text="Admin account",var=varAdmin)
    chkAdmin.place(x=320,y=80)
    
    varCalculator = BooleanVar()
    chkCalculator = Checkbutton(win,text="Use calculator",var=varCalculator)
    chkCalculator.place(x=320,y=120)

    btnBack = Button(win,width=10,text="Back",command=lambda:openLogin(win))
    btnBack.place(x=200,y=160)

    btnSignup = Button(win,width=10,text="Sign up",command=lambda:clickSignup(win,entUsername,entPassword,varGender,cmbNationality,varAdmin,varCalculator))
    btnSignup.place(x=300,y=160)

    mainloop()

# ============ Calculator =================
a = 0
b = 0
sym = None
expression = ""

def openCalculator(win):
    win.destroy()
    calculatorScreen()

def press(num,lb):
    global expression, sym, a, b

    if (num=="AC"):
        clearAll()
    elif (num=='='):
        calculate()
    elif (num=="+" or num=='-' or num=='*' or num=='/'):
        if (sym!=None):
            calculate()
        sym=num
        expression+=num
    else:
        if (sym!=None):
            b=b*10+int(num)
        else:
            a=a*10+int(num)
        expression+=num

    lb.configure(text=expression)

def calculate():
    global a, b, sym, expression

    if (sym=='+'):
        a+=b
    elif (sym=='-'):
        a-=b
    elif (sym=='*'):
        a*=b
    elif (sym=='/'):
        if (b==0):
            messagebox.showerror("Error","Cannot divided by zero")
        else:
            a//=b
    
    b=0
    sym=None
    expression=str(a)

def clearAll():
    global a,b,sym,expression
    a=0
    b=0
    sym=None
    expression=""

def calculatorScreen():
    win = Tk()
    win.title("Calculator")

    #Menu
    mainMenu = Menu(win)
    optionMenu = Menu(mainMenu,tearoff=0)
    win.configure(menu=mainMenu)
    mainMenu.add_cascade(label="Option",menu=optionMenu)
    optionMenu.add_command(label="Back",command=lambda:openMenu(win))
    
    #Row 0
    result = Label(win,bg='white',borderwidth=2,relief="groove")
    result.grid(column=1,row=1,columnspan=4,sticky="we",ipady=5)

    #Row 1
    btn7 = Button(win,bg="lightgreen",text="7",width=5,height=3,command=lambda:press("7",result))
    btn7.grid(column=1,row=2)

    btn8 = Button(win,bg="lightgreen",text="8",width=5,height=3,command=lambda:press("8",result))
    btn8.grid(column=2,row=2)

    btn9 = Button(win,bg="lightgreen",text="9",width=5,height=3,command=lambda:press("9",result))
    btn9.grid(column=3,row=2)

    btnPlus = Button(win,bg="medium purple",text="=",width=5,command=lambda:press("=",result))
    btnPlus.grid(column=4,row=2,sticky="ns")

    #Row 2
    btn4 = Button(win,bg="yellow",text="4",width=5,height=3,command=lambda:press("4",result))
    btn4.grid(column=1,row=3)

    btn5 = Button(win,bg="yellow",text="5",width=5,height=3,command=lambda:press("5",result))
    btn5.grid(column=2,row=3)

    btn6 = Button(win,bg="yellow",text="6",width=5,height=3,command=lambda:press("6",result))
    btn6.grid(column=3,row=3)
    
    btnAC = Button(win,bg="medium purple",text="AC",width=5,command=lambda:press('AC',result))
    btnAC.grid(column=4,row=3,sticky="ns")

    #Row 3
    btn1 = Button(win,bg="lightblue",text="1",width=5,height=3,command=lambda:press("1",result))
    btn1.grid(column=1,row=4)

    btn2 = Button(win,bg="lightblue",text="2",width=5,height=3,command=lambda:press("2",result))
    btn2.grid(column=2,row=4)

    btn3 = Button(win,bg="lightblue",text="3",width=5,height=3,command=lambda:press("3",result))
    btn3.grid(column=3,row=4)
    
    btn0 = Button(win,bg="medium purple",text="0",width=5,command=lambda:press('0',result))
    btn0.grid(column=4,row=4,sticky="ns")

    #Row 4
    btnDiv = Button(win,bg="pink",text="/",width=5,height=3,command=lambda:press("/",result))
    btnDiv.grid(column=1,row=5)

    btnMul = Button(win,bg="pink",text="*",width=5,height=3,command=lambda:press("*",result))
    btnMul.grid(column=2,row=5)

    btnSub = Button(win,bg="pink",text="-",width=5,height=3,command=lambda:press("-",result))
    btnSub.grid(column=3,row=5)
    
    btnPlus = Button(win,bg="pink",text="+",width=5,command=lambda:press('+',result))
    btnPlus.grid(column=4,row=5,sticky="ns")

    mainloop()

# ============ Create item ================
def clickCreate(entItemName,entPrice):
    try:
        itemName = clearSpecial(entItemName.get())
        price = int(entPrice.get())
        assert (price>=0)
    except:
        messagebox.showerror("Error","Please check again the input")
        return None

    if (checkExistItem(itemName)!=None):
        messagebox.showerror("Create result","Cannot create item whose name are same")
        return None

    regex = "%s|%d"
    appendFile(itemFilePath,regex%(itemName,price))
    messagebox.showinfo("Create result","Created successfully item")

def createItemScreen():
    win = Tk()
    win.title("Create a new item")

    loadItemList(itemFilePath)

    frame = Frame(win)
    frame.pack(padx=5,pady=5)

    lbTitle = Label(frame,text="Create a new item",font=("Arial",15),foreground=headingColor)
    lbTitle.grid(row=1,column=1,columnspan=2,sticky="WE")

    lbItemName = Label(frame,text="Item name")
    lbItemName.grid(row=2,column=1,sticky="W")
    entItemName = Entry(frame,width=10)
    entItemName.grid(row=2,column=2)

    lbPrice = Label(frame,text="Price ($)")
    lbPrice.grid(row=3,column=1,sticky="W")
    entPrice = Entry(frame,width=10)
    entPrice.grid(row=3,column=2)

    btnBack = Button(frame,text="Back",width=15,command=lambda:openMenu(win))
    btnBack.grid(row=5,column=1)

    btnCreate = Button(frame,text="Create",width=15,command=lambda:clickCreate(entItemName,entPrice))
    btnCreate.grid(row=5,column=2)

    mainloop()

# ============ Delete item ================
def clickDelete(cmbItemName):
    itemName = cmbItemName.get()
    item = checkExistItem(itemName)
    if (item!=None):
        listItem.remove(item)
        writeListItem(itemFilePath)
        messagebox.showinfo("Delete result","Item deleted successfully")
    else:
        messagebox.showerror("Delete result","Item does not exist, please try again")
    loadComboName(cmbItemName)

def getListItemName():
    result = []
    for item in listItem:
        result.append(item.name)
    return result

def loadComboName(cmb):
    loadItemList(itemFilePath)

    listName = getListItemName()
    cmb.configure(values=listName)
    if (len(listName)>0):
        cmb.current(0)  
    
def deleteItemScreen():
    win = Tk()
    win.title("Delete an item")
    
    frame = Frame(win)
    frame.pack(padx=5,pady=5)

    lbTitle = Label(frame,text="Delete an item",font=("Arial",15),foreground=headingColor)
    lbTitle.grid(row=1,column=1,columnspan=2,sticky="WE")  

    lbSelectItem = Label(frame,text="Select an item")
    lbSelectItem.grid(row=2,column=1,stick='W')

    cmbItemName = Combobox(frame,state="readonly")
    loadComboName(cmbItemName)
    cmbItemName.grid(row=2,column=2,stick='WE')

    btnBack = Button(frame,text="Back",width=10,command=lambda:openMenu(win))
    btnBack.grid(row=3,column=1,stick='WE')

    btnDelete = Button(frame,text="Delete",width=10,command=lambda:clickDelete(cmbItemName))
    btnDelete.grid(row=3,column=2,stick='WE')

    mainloop()

# ============ Billing system (add item, create bill) ==================
def clickAdd(cmbItemName,entAmount,lbCart,cart):
    try:
        itemName = cmbItemName.get()
        amount = int(entAmount.get())
        item = checkExistItem(itemName)
        assert(item!=None)
        assert(amount>=0)
    except:
        messagebox.showerror("Error","Please check again the input")
        return None 
    cart.add(item, amount)
    lbCart.configure(text=str(cart))

def clickConfirm(win,lbCart,cart):
    try:
        money = int(simpledialog.askstring("Bill", "How much does customer give you ($)?",parent=win))
    except:
        messagebox.showerror("Bill","Please check your input")
        return None

    total = cart.total()
    if (money<total):
        messagebox.showerror("Bill","The money is not enough")
        return None
    else:
        s = "Payment successfully\n"
        s+= "Change money: %d$"%(money-total)
        messagebox.showinfo("Bill",s)
        cart.clear()
        lbCart.configure(text=str(cart))
        currentAccount.money+=total
        writeListAccount(accountFilePath)

def billingScreen():
    win = Tk()
    win.title("Billing system")

    cart = Cart()

    frame = Frame(win)
    frame.pack(padx=5,pady=5)

    lbTitle = Label(frame,text="Billing system",font=("Arial",15),foreground=headingColor)
    lbTitle.grid(row=1,column=1,columnspan=2,sticky="WE")  

    lbSelectItem = Label(frame,text="Select an item")
    lbSelectItem.grid(row=2,column=1,stick='W')

    cmbItemName = Combobox(frame,state="readonly",width=17)
    loadComboName(cmbItemName)
    cmbItemName.grid(row=2,column=2,stick='WE')
    
    lbSelectItem = Label(frame,text="Amount:")
    lbSelectItem.grid(row=3,column=1,stick='W')

    entAmount = Entry(frame,width=20)
    entAmount.grid(row=3,column=2)

    lbCart = Label(frame,justify="left",relief="solid",borderwidth=2,anchor='w')
    lbCart.grid(row=4,column=1,columnspan=2,stick="WE")
    lbCart.configure(text=str(cart))

    btnBack = Button(frame,text="Back",width=10,command=lambda:openMenu(win))
    btnBack.grid(row=5,column=1,stick='WE')

    btnAdd = Button(frame,text="Add",width=10,command=lambda:clickAdd(cmbItemName,entAmount,lbCart,cart))
    btnAdd.grid(row=5,column=2,stick='WE')

    btnConfirm = Button(frame,text="Confirm",command=lambda:clickConfirm(win,lbCart,cart))
    btnConfirm.grid(row=6,column=1,columnspan=2,stick='WE')

    mainloop()

# ============ Main driven ================
def main():
    loginScreen()

if __name__=="__main__":
    main()