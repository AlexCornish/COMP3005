import psycopg2
import tkinter
import copy
from datetime import datetime, timedelta

def addToTable(tableName):
    if tableName == "book":
       addBookManually() 

def getMaxAddressID():
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("select max(address_id) from address")
    record = cur.fetchall()
    cur.close()
    result = int(record[0][0]) + 1
    return result

def generateNewUserID():
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("select max(user_id) from customer")
    record = cur.fetchall()
    cur.close()
    if record[0][0] != None:
        result = int(record[0][0]) + 1
        return result
    else:
        return 1

def all_children(window):
    listOfChildren = window.winfo_children()
    for item in listOfChildren:
        if item.winfo_children:
            listOfChildren.extend(item.winfo_children())
    return listOfChildren

def clearScreen():
    listOfChildren = root.winfo_children()
    for item in listOfChildren:
        if item.winfo_children:
            listOfChildren.extend(item.winfo_children())
    for i in listOfChildren:
        i.pack_forget()

def checkIfUserExists(idToCheck):
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    query = "select * from customer where user_id=%d" %(idToCheck)
    cur.execute(query)
    record = cur.fetchall()
    cur.close()
    if len(record) == 1:
        return record
    else:
        return False

def loadUserFromMain(arg):
    currentUser = int(entry.get())
    newRec = checkIfUserExists(currentUser)
    if newRec == False:
        None
    else:
        clearScreen()
        mainPage(arg,newRec)

def loadSearchPage(arg,value,value1, newRec):
    currentUser = newRec
    clearScreen()
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    query = ""
    if value1 == 'Book Name':
        query = "select * from book where book_name='%s'" %(value)
    elif value1 == 'Author Name':
        query = "select * from book where author_name='%s'" %(value)
    elif value1 == 'ISBN':
        query = "select * from book where isbn=%d" %(value)
    elif value1 == 'Genre':
        query = "select * from book where genre='%s'" %(value)
    cur.execute(query)
    record = cur.fetchall()
    cur.close()
    frame1 = tkinter.Frame(root)
    frame1.pack()
    nameStr = "Hello %s" %(currentUser[0][1])
    newLabel = tkinter.Label(frame1, text=nameStr)
    newLabel.pack(side=tkinter.TOP)
    SEARCHTYPE = [
        'Book Name',
        'Author Name',
        'ISBN',
        'Genre',
    ]
    variable = tkinter.StringVar(root)
    variable.set(SEARCHTYPE[0])
    dropdown = tkinter.OptionMenu(root, variable, *SEARCHTYPE)
    dropdown.pack()
    dropdown.place(x=20, y=20)
    basketButton = tkinter.Button(frame1,text="Basket")
    basketButton.bind('<Button-1>', lambda event: loadBasket(root, newRec))
    basketButton.pack()
    basketButton.place(x=300, y=20)
    entry1 = tkinter.Entry(frame1)
    entry1.pack(side=tkinter.TOP)
    b1 = tkinter.Button(frame1,text="Search")
    b1.bind('<Button-1>', lambda event: loadSearchPage(root, entry1.get(),variable.get(),newRec))
    b1.pack(side=tkinter.TOP)
    for i in range(0,len(record)):
        strText = str(i+1) + ": " + str(record[i][0]) + "      Author: " + str(record[i][1]) + "      ISBN: " + str(record[i][2]) + "   Genre: " + str(record[i][3])
        newButton = tkinter.Button(frame1,text=strText)
        newButton.bind('<Button-1>')
        newButton.pack()
    entry2 = tkinter.Entry(frame1)
    entry2.pack()
    b1 = tkinter.Button(frame1,text="Load Book Page by Index")
    b1.bind('<Button-1>', lambda event: loadBookPage(root, record[int(entry2.get())-1],newRec))
    b1.pack(side=tkinter.BOTTOM)
        
def loadBasket(arg, newRec):
    clearScreen()
    frame1 = tkinter.Frame(root)
    frame1.pack()
    
    newLabel = tkinter.Label(frame1, text="Basket: ")
    newLabel.pack(side=tkinter.TOP)
    mainMenu = tkinter.Button(frame1,text="Main Menu")
    mainMenu.bind('<Button-1>', lambda event: mainPage(root, newRec))
    mainMenu.pack()
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    query = "select * from book natural join userBasket where user_id=%d" %(newRec[0][0])
    cur.execute(query)
    record = cur.fetchall()
    for i in range(0,len(record)):
        strText = str(i+1) + ": " + str(record[i][1]) + "      Author: " + str(record[i][2]) + "      ISBN: " + str(record[i][0]) + "   Genre: " + str(record[i][3] + " $" + str(record[i][6]))
        newButton = tkinter.Button(frame1,text=strText)
        newButton.pack()
    query = "select sum(price) from book natural join userBasket where user_id=%d" %(newRec[0][0])
    cur.execute(query)
    record1 = cur.fetchall()
    cur.close()
    entry1 = tkinter.Entry(frame1)
    entry1.pack()
    b1 = tkinter.Button(frame1,text="Load Book Page by Index")
    b1.bind('<Button-1>', lambda event: loadBookPageFromBasket(root, record[int(entry1.get())-1],newRec))
    b1.pack()

    buttonText = "Checkout Basket $%s" %(record1[0])
    b2 = tkinter.Button(frame1,text=buttonText)
    b2.bind('<Button-1>', lambda event: makeOrder(root, newRec))
    b2.pack()


def generateNewOrderID():
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("select max(ordernum) from orderInfo")
    record = cur.fetchall()
    cur.close()
    if record[0][0] != None:
        result = int(record[0][0]) + 1
        return result
    else:
        return 1

def generateNewTrackingID():
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute("select max(trackingnum) from orderInfo")
    record = cur.fetchall()
    cur.close()
    if record[0][0] != None:
        result = int(record[0][0]) + 1
        return result
    else:
        return 1

def makeOrder(root, user):
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    # Get books from basket
    query = "select * from book natural join userBasket where user_id=%d" %(user[0][0])
    cur.execute(query)
    record = cur.fetchall()
    # Create New Order
    trackingID = generateNewTrackingID()
    orderID = generateNewOrderID()
    orderInfoQuery = """ INSERT INTO orderInfo (ordernum, trackingnum, orderdate) VALUES (%s,%s,%s)"""
    orderQuery = (orderID, trackingID, datetime.today().strftime('%Y-%m-%d'))
    cur.execute(orderInfoQuery, orderQuery)
    cur.close()
    conn.commit()
    # Create userOrderObject 
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    userOrderInfoQuery = """ INSERT INTO userOrder(user_id, ordernum) VALUES (%s,%s)"""
    userOrderQuery = (user[0][0], orderID)
    cur.execute(userOrderInfoQuery, userOrderQuery)
    cur.close()
    conn.commit()
    #Create bookOrderObjects
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    bookOrderQuery = """select ISBN from userBasket where user_id=%d""" %(user[0][0])
    cur.execute(bookOrderQuery)
    record4 = cur.fetchall()
    cur.close()
    for each in record4:
        conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
        cur = conn.cursor()
        bookOrderInfoQuery = """ INSERT INTO bookOrder(ordernum, isbn) VALUES (%s,%s)"""
        bookOrderInQuery = (orderID,each)
        cur.execute(bookOrderInfoQuery, bookOrderInQuery)
        cur.close()
        conn.commit()
    # Get total of books
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    query = "select sum(price) from book natural join userBasket where user_id=%d" %(user[0][0])
    cur.execute(query)
    record1 = cur.fetchall()
    cur.close()
    #Update Quantity of Books
    for individualBook in record4:
        query123 = "update book set quantity = quantity - 1 where isbn = %d" %(individualBook[0])
        conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
        cur = conn.cursor()
        cur.execute(query123)
        cur.close()
        conn.commit()
        queryCheck = "select * from book where quantity < 10 and isbn=%d" %(individualBook[0])
        conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
        cur = conn.cursor()
        cur.execute(queryCheck)
        record59 = cur.fetchone()
        if record59 != None:
            value = getBooksSoldThisMonth(individualBook[0])
            query12 = "update book set quantity = quantity + %d where isbn = %d" %(value, individualBook[0])
            conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
            cur = conn.cursor()
            cur.execute(query12)
            cur.close()
            conn.commit()
        cur.close()
    #Figure out share for each publisher
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    newQuery = """select publisher, sum(0.25 * price) from book natural join userBasket group by publisher"""
    cur.execute(newQuery)
    record2 = cur.fetchall()
    cur.close()
    conn.commit()
    for i in record2:
        conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
        cur = conn.cursor()
        query1 = "select bankAccount_id from bookPublisher where name='%s'" %(i[0])
        cur.execute(query1)
        record3 = cur.fetchall()
        query2 = "update bankAccount set balance = balance + %f where bankaccount_id=%s" %(i[1],record3[0][0])
        cur.execute(query2)
        cur.close()
        conn.commit()
    cur.close()
    # Clear user basket
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    query = "delete from userBasket where user_id=%d" %(user[0][0])
    cur.execute(query)
    cur.close()
    conn.commit()
    

def addToBasket2(arg,user,book):
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    userBasketQuery = """ INSERT INTO userBasket (user_id, isbn) VALUES (%s,%s)"""
    userBasketObj = (user[0][0], book[2])
    cur = conn.cursor()
    cur.execute(userBasketQuery, userBasketObj)
    cur.close()
    conn.commit()

def loadBookPageFromBasket(arg, record,newRec):
    query = "select * from book where isbn=%d" %(record[0])
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute(query)
    record2 = cur.fetchall()
    cur.close()
    loadBookPage(arg,record2[0],newRec)

def loadBookPage(arg, record,newRec):
    clearScreen()
    frame1 = tkinter.Frame(root)
    frame1.pack()

    basketButton = tkinter.Button(frame1,text="Add to Basket")
    basketButton.bind('<Button-1>', lambda event: addToBasket2(root, newRec, record))
    basketButton.pack(side=tkinter.BOTTOM)

    addToBasket = tkinter.Button(frame1,text="View Basket")
    addToBasket.bind('<Button-1>', lambda event: loadBasket(root, newRec))
    addToBasket.pack(side=tkinter.BOTTOM)

    mainMenu = tkinter.Button(frame1,text="Main Menu")
    mainMenu.bind('<Button-1>', lambda event: mainPage(root, newRec))
    mainMenu.pack(side=tkinter.BOTTOM)

    bookTitle = "Title: %s" %(record[0])
    bookTitleLabel = tkinter.Label(frame1,text=bookTitle)
    bookTitleLabel.pack()

    bookAuthor = "Author: %s" %(record[1])
    bookAuthorLabel = tkinter.Label(frame1,text=bookAuthor)
    bookAuthorLabel.pack()

    bookISBN = "ISBN: %s" %(record[2])
    bookISBNLabel = tkinter.Label(frame1,text=bookISBN)
    bookISBNLabel.pack()
    
    bookGenre = "Genre: %s" %(record[3])
    bookGenreLabel = tkinter.Label(frame1,text=bookGenre)
    bookGenreLabel.pack()

    bookPublisher = "Publisher: %s" %(record[4])
    bookPublisherLabel = tkinter.Label(frame1,text=bookPublisher)
    bookPublisherLabel.pack()

    bookPages = "Number of Pages: %s" %(record[5])
    bookPagesLabel = tkinter.Label(frame1,text=bookPages)
    bookPagesLabel.pack()
    
    bookPrice = "Price: %s" %(record[6])
    bookPriceLabel = tkinter.Label(frame1,text=bookPrice)
    bookPriceLabel.pack()

    bookStock = "Number in left stock: %s" %(record[7])
    bookStockLabel = tkinter.Label(frame1,text=bookStock)
    bookStockLabel.pack()

def viewProfile(arg,newRec):
    clearScreen()
    frame1 = tkinter.Frame(root)
    frame1.pack()
    currentUser = newRec
    clearScreen()
    frame1 = tkinter.Frame(root)
    frame1.pack()
    nameStr = "Hello %s" %(currentUser[0][1])
    newLabel = tkinter.Label(frame1, text=nameStr)
    newLabel.pack()
    SEARCHTYPE = [
        'Book Name',
        'Author Name',
        'ISBN',
        'Genre',
    ]
    variable = tkinter.StringVar(root)
    variable.set(SEARCHTYPE[0])
    dropdown = tkinter.OptionMenu(root, variable, *SEARCHTYPE)
    dropdown.pack()
    entry1 = tkinter.Entry(frame1)
    entry1.pack()
    
    b1 = tkinter.Button(frame1,text="Search")
    b1.bind('<Button-1>', lambda event: loadSearchPage(root, entry1.get(),variable.get(),newRec))
    b1.pack()
    mainMenu = tkinter.Button(frame1,text="Main Menu")
    mainMenu.bind('<Button-1>', lambda event: mainPage(arg, newRec))
    mainMenu.pack()
    addToBasket = tkinter.Button(frame1,text="View Basket")
    addToBasket.bind('<Button-1>', lambda event: loadBasket(root, newRec))
    addToBasket.pack()
    newLabel = tkinter.Label(frame1, text="YOUR ORDERS")
    newLabel.pack()
    query = "select * from userOrder natural join orderInfo where user_id=%d" %(newRec[0][0])
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute(query)
    record2 = cur.fetchall()
    cur.close()
    for i in range(0,len(record2)):
        strText = str(i+1) + ":     Order Number: " + str(record2[i][0]) + "     Tracking Number: " + str(record2[i][2]) + "     Order Date: " + str(record2[i][3])
        newButton = tkinter.Button(frame1,text=strText)
        newButton.pack()
    entry1 = tkinter.Entry(frame1)
    entry1.pack()
    b1 = tkinter.Button(frame1,text="Load Order by Index")
    b1.bind('<Button-1>', lambda event: viewOrder(root,newRec, record2[int(entry1.get())-1][0]))
    b1.pack()

def viewOrder(arg, newRec, orderNum):
    clearScreen()
    frame1 = tkinter.Frame(root)
    frame1.pack()
    currentUser = newRec
    clearScreen()
    frame1 = tkinter.Frame(root)
    frame1.pack()
    nameStr = "Hello %s" %(currentUser[0][1])
    newLabel = tkinter.Label(frame1, text=nameStr)
    newLabel.pack()
    SEARCHTYPE = [
        'Book Name',
        'Author Name',
        'ISBN',
        'Genre',
    ]
    variable = tkinter.StringVar(root)
    variable.set(SEARCHTYPE[0])
    dropdown = tkinter.OptionMenu(root, variable, *SEARCHTYPE)
    dropdown.pack()
    entry1 = tkinter.Entry(frame1)
    entry1.pack()
    
    b1 = tkinter.Button(frame1,text="Search")
    b1.bind('<Button-1>', lambda event: loadSearchPage(root, entry1.get(),variable.get(),newRec))
    b1.pack()
    mainMenu = tkinter.Button(frame1,text="Main Menu")
    mainMenu.bind('<Button-1>', lambda event: mainPage(arg, newRec))
    mainMenu.pack()
    addToBasket = tkinter.Button(frame1,text="View Basket")
    addToBasket.bind('<Button-1>', lambda event: loadBasket(root, newRec))
    addToBasket.pack()
    orderText = "NOW SHOWING ORDER #" + str(orderNum)
    newLabel = tkinter.Label(frame1, text=orderText)
    newLabel.pack()
    query = "select * from bookOrder natural join book where orderNum=%s" %(orderNum)
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute(query)
    record2 = cur.fetchall()
    cur.close()
    for i in range(0,len(record2)):
        strText = str(i+1) + ":   Title: " + str(record2[i][2]) + "     Author Name: " + str(record2[i][3]) + "     ISBN: " + str(record2[i][0])
        newButton = tkinter.Button(frame1,text=strText)
        newButton.pack()
    entry1 = tkinter.Entry(frame1)
    entry1.pack()
    b1 = tkinter.Button(frame1,text="Load Book Page by Index")
    b1.bind('<Button-1>', lambda event: loadBookPageFromBasket(root, record2[int(entry1.get())-1],newRec))
    b1.pack()
    

def mainPage(arg,newRec):
    currentUser = newRec
    clearScreen()
    frame1 = tkinter.Frame(root)
    frame1.pack()
    nameStr = "Hello %s" %(currentUser[0][1])
    newLabel = tkinter.Label(frame1, text=nameStr)
    newLabel.pack()
    SEARCHTYPE = [
        'Book Name',
        'Author Name',
        'ISBN',
        'Genre',
    ]
    variable = tkinter.StringVar(root)
    variable.set(SEARCHTYPE[0])
    dropdown = tkinter.OptionMenu(root, variable, *SEARCHTYPE)
    dropdown.pack(side=tkinter.TOP)
    entry1 = tkinter.Entry(frame1)
    entry1.pack(side=tkinter.LEFT)
    
    b1 = tkinter.Button(frame1,text="Search")
    b1.bind('<Button-1>', lambda event: loadSearchPage(root, entry1.get(),variable.get(),newRec))
    b1.pack(side=tkinter.LEFT)

    addToBasket = tkinter.Button(frame1,text="View Basket")
    addToBasket.bind('<Button-1>', lambda event: loadBasket(root, newRec))
    addToBasket.pack(side=tkinter.BOTTOM)

    customerProfile = tkinter.Button(frame1,text="View Profile")
    customerProfile.bind('<Button-1>', lambda event: viewProfile(root, newRec))
    customerProfile.pack(side=tkinter.BOTTOM)

def createNewUserInsertInfo(arg, userID,userName, billingAddress_id, billingAddressStreetNum, billingAddressStreetName, billingAddressCity, billingAddressCountry, billingAddressPostCode, deliveryAddress_id, deliveryAddressStreetNum, deliveryAddressStreetName, deliveryAddressCity, deliveryAddressCountry, deliveryAddresspostCode):
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    
   
    user = (userID, userName)
    userQuery = """ INSERT INTO customer (user_id, name) VALUES (%s,%s)"""
    cur.execute(userQuery, user)


    Address = (billingAddress_id, billingAddressStreetNum, billingAddressStreetName, billingAddressCity, billingAddressCountry, billingAddressPostCode)
    billingAddressQuery = """ INSERT INTO address (address_id, streetNum, streetName, city, country, postcode) VALUES (%s,%s,%s,%s,%s,%s)"""
    cur.execute(billingAddressQuery, Address)

    billingAddress = (userID, billingAddress_id)
    billingAddressQuery1 = """ INSERT INTO billingAddress (user_id, address_id) VALUES (%s,%s)"""
    cur.execute(billingAddressQuery1, billingAddress)

    addressForDelivery = (deliveryAddress_id, deliveryAddressStreetNum, deliveryAddressStreetName, deliveryAddressCity, deliveryAddressCountry, deliveryAddresspostCode)
    deliveryAddressQuery = """ INSERT INTO address (address_id, streetNum, streetName, city, country, postcode) VALUES (%s,%s,%s,%s,%s,%s)"""
    cur.execute(deliveryAddressQuery, addressForDelivery)

    deliveryAddress = (userID, deliveryAddress_id)
    deliveryAddressQuery1 = """ INSERT INTO deliveryAddress (user_id, address_id) VALUES (%s,%s)"""
    cur.execute(deliveryAddressQuery1, deliveryAddress)
    cur.close()
    conn.commit()
    clearScreen()


def createNewUser(arg):
    clearScreen()
    frame1 = tkinter.Frame(root)
    frame1.pack()
    t2 = tkinter.Label(frame1, text="NEW USER CREATION PAGE")
    t2.pack()
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    userID = generateNewUserID()
    newUsernameLabel = tkinter.Label(frame1, text="Name:")
    newUsernameLabel.pack()
    newUsername = tkinter.Entry(frame1)
    newUsername.pack()


    billingAddress_id = getMaxAddressID()

    billingAddressLabel = tkinter.Label(frame1, text="Billing Address info")
    billingAddressLabel.pack()

    billingAddressStreetNumLabel = tkinter.Label(frame1, text="Street Num:")
    billingAddressStreetNumLabel.pack()
    billingAddressStreetNum = tkinter.Entry(frame1)
    billingAddressStreetNum.pack()

    billingAddressStreetNameLabel = tkinter.Label(frame1, text="Street Name:")
    billingAddressStreetNameLabel.pack()
    billingAddressStreetName = tkinter.Entry(frame1)
    billingAddressStreetName.pack()

    billingAddressCityLabel = tkinter.Label(frame1, text="City:")
    billingAddressCityLabel.pack()
    billingAddressCity = tkinter.Entry(frame1)
    billingAddressCity.pack()
    
    billingAddressCountryLabel = tkinter.Label(frame1, text="Country:")
    billingAddressCountryLabel.pack()
    billingAddressCountry = tkinter.Entry(frame1)
    billingAddressCountry.pack()

    billingAddresspostCodeLabel = tkinter.Label(frame1, text="Postcode:")
    billingAddresspostCodeLabel.pack()
    billingAddressPostCode = tkinter.Entry(frame1)
    billingAddressPostCode.pack()
    
    deliveryAddress_id = getMaxAddressID() + 1

    deliveryAddressLabel = tkinter.Label(frame1, text="Delivery Address info")
    deliveryAddressLabel.pack()

    deliveryAddressStreetNumLabel = tkinter.Label(frame1, text="Street Num:")
    deliveryAddressStreetNumLabel.pack()
    deliveryAddressStreetNum = tkinter.Entry(frame1)
    deliveryAddressStreetNum.pack()

    deliveryAddressStreetNameLabel = tkinter.Label(frame1, text="Street Name:")
    deliveryAddressStreetNameLabel.pack()
    deliveryAddressStreetName = tkinter.Entry(frame1)
    deliveryAddressStreetName.pack()

    deliveryAddressCityLabel = tkinter.Label(frame1, text="City:")
    deliveryAddressCityLabel.pack()
    deliveryAddressCity = tkinter.Entry(frame1)
    deliveryAddressCity.pack()
    
    deliveryAddressCountryLabel = tkinter.Label(frame1, text="Country:")
    deliveryAddressCountryLabel.pack()
    deliveryAddressCountry = tkinter.Entry(frame1)
    deliveryAddressCountry.pack()

    deliveryAddresspostCodeLabel = tkinter.Label(frame1, text="Postcode:")
    deliveryAddresspostCodeLabel.pack()
    deliveryAddresspostCode = tkinter.Entry(frame1)
    deliveryAddresspostCode.pack()

    enterBut = tkinter.Button(frame1,text="Enter")
    enterBut.bind('<Button-1>', lambda event: createNewUserInsertInfo(root, userID, newUsername.get(),billingAddress_id, billingAddressStreetNum.get(), billingAddressStreetName.get(), billingAddressCity.get(), billingAddressCountry.get(), billingAddressPostCode.get(),deliveryAddress_id, deliveryAddressStreetNum.get(), deliveryAddressStreetName.get(), deliveryAddressCity.get(), deliveryAddressCountry.get(), deliveryAddresspostCode.get()))
    enterBut.pack()
   
def addBookManually(root,recordNew): 
    clearScreen()
    frame1 = tkinter.Frame(root)
    frame1.pack()
    t2 = tkinter.Label(frame1, text="ADD BOOK TO SELECTION")
    t2.pack()
    bookNameLabel = tkinter.Label(frame1, text="Book Name:")
    bookNameLabel.pack()
    bookName = tkinter.Entry(frame1)
    bookName.pack()

    bookAuthorLabel = tkinter.Label(frame1, text="Author Name:")
    bookAuthorLabel.pack()
    bookAuthor = tkinter.Entry(frame1)
    bookAuthor.pack()

    bookISBNLabel = tkinter.Label(frame1, text="ISBN:")
    bookISBNLabel.pack()
    bookISBN = tkinter.Entry(frame1)
    bookISBN.pack()

    bookGenreLabel = tkinter.Label(frame1, text="Genre:")
    bookGenreLabel.pack()
    bookGenre = tkinter.Entry(frame1)
    bookGenre.pack()

    bookPublisherLabel = tkinter.Label(frame1, text="Publisher:")
    bookPublisherLabel.pack()
    bookPublisher = tkinter.Entry(frame1)
    bookPublisher.pack()

    booknumPageLabel = tkinter.Label(frame1, text="Number of Pages:")
    booknumPageLabel.pack()
    booknumPage = tkinter.Entry(frame1)
    booknumPage.pack()

    bookPriceLabel = tkinter.Label(frame1, text="Price:")
    bookPriceLabel.pack()
    bookPrice = tkinter.Entry(frame1)
    bookPrice.pack()

    bookQuantityLabel = tkinter.Label(frame1, text="Quantity:")
    bookQuantityLabel.pack()
    bookQuantity = tkinter.Entry(frame1)
    bookQuantity.pack()
    insertBook2 = tkinter.Button(frame1,text="Add Book")
    insertBook2.bind('<Button-1>', lambda event: insertBook(root,recordNew,bookName.get(),bookAuthor.get(), bookISBN.get(), bookGenre.get(),bookPublisher.get(),booknumPage.get(),bookPrice.get(),bookQuantity.get()))
    insertBook2.pack()
    returnToMain = tkinter.Button(frame1,text="Owner Main Menu")
    returnToMain.bind('<Button-1>', lambda event: loadOwnerFromMain(root,recordNew[0]))
    returnToMain.pack()


def insertBook(root,owner, name,author,ISBN,genre,publisher,numPages, price, quantity):
    frame1 = tkinter.Frame(root)
    frame1.pack()
    query = """ INSERT INTO book (book_Name, author_Name, ISBN, genre, publisher, numPages, price, quantity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    toInsert = (name,author, ISBN, genre, publisher,numPages,price,quantity)
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute(query,toInsert)
    cur.close()
    conn.commit()
    clearScreen()
    ownerMainMenu(owner)

def deleteBook(root, owner, ISBNToDelete):
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    query = "delete from book where isbn=%s" %(ISBNToDelete)
    cur.execute(query)
    cur.close()
    conn.commit()
    clearScreen()
    ownerMainMenu(owner)


def removeBookManually(root,recordNew):
    clearScreen()
    frame1 = tkinter.Frame(root)
    frame1.pack()
    t2 = tkinter.Label(frame1, text="NEW BOOK DELETION PAGE")
    t2.pack()
    
    bookISBNLabel = tkinter.Label(frame1, text="ISBN:")
    bookISBNLabel.pack()
    bookISBN = tkinter.Entry(frame1)
    bookISBN.pack()

    deleteBook2 = tkinter.Button(frame1,text="Delete Book")
    deleteBook2.bind('<Button-1>', lambda event: deleteBook(root,recordNew,bookISBN.get()))
    deleteBook2.pack()
    returnToMain = tkinter.Button(frame1,text="Cancel Deletion")
    returnToMain.bind('<Button-1>', lambda event: loadOwnerFromMain(root,recordNew[0]))
    returnToMain.pack()

def displayPublisherInfo(root, recordNew):
    clearScreen()
    frame1 = tkinter.Frame(root)
    frame1.pack()
    t2 = tkinter.Label(frame1, text="PUBLISHERS")
    t2.pack()
    query = "select * from bookPublisher"
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute(query)
    record2 = cur.fetchall()
    cur.close()
    for i in range(0,len(record2)):
        strText = str(i+1) + ": " + str(record2[i][0]) + "      Email: " + str(record2[i][2]) + "      Phone Num: " + str(record2[i][3])
        newButton = tkinter.Button(frame1,text=strText)
        newButton.pack()
    entry1 = tkinter.Entry(frame1)
    entry1.pack()
    b1 = tkinter.Button(frame1,text="Load Publisher Page by Index")
    b1.bind('<Button-1>', lambda event: loadPublisherPage(root, record2[int(entry1.get())-1],recordNew))
    b1.pack()
    returnToMain = tkinter.Button(frame1,text="Owner Main Menu")
    returnToMain.bind('<Button-1>', lambda event: loadOwnerFromMain(root,recordNew[0]))
    returnToMain.pack()

def loadPublisherPage(arg,publisherInfo, user):
    query = "select * from bookPublisher natural join bankAccount natural join address where name='%s'" %(publisherInfo[0])
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute(query)
    recordNew = cur.fetchone()
    clearScreen()
    cur.close()
    conn.commit()
    frame1 = tkinter.Frame(root)
    frame1.pack()
    t2 = tkinter.Label(frame1, text=recordNew[2])
    t2.pack()
    returnToMain = tkinter.Button(frame1,text="Owner Main Menu")
    returnToMain.bind('<Button-1>', lambda event: loadOwnerFromMain(root,user[0]))
    returnToMain.pack()
    addressStr = "Address: " + str(recordNew[6]) + " " +  str(recordNew[7]) + " " + str(recordNew[8]) + ", " + str(recordNew[9]) + " " + str(recordNew[10])
    addressLabel = tkinter.Label(frame1, text=addressStr)
    addressLabel.pack()
    emailStr = "Email: " + str(recordNew[3])
    emailLabel = tkinter.Label(frame1, text=emailStr)
    emailLabel.pack()
    phoneNum = "Phone Number: " + str(recordNew[4])
    phoneNumLabel = tkinter.Label(frame1, text=phoneNum)
    phoneNumLabel.pack()
    moneySent = "Money Given: $" + str(recordNew[5])
    moneySentLabel = tkinter.Label(frame1, text=moneySent)
    moneySentLabel.pack()
    bookTitleLabel = tkinter.Label(frame1, text="Books Published:")
    bookTitleLabel.pack()
    selectByPublisherQuery = "select * from book where publisher='%s'" %(recordNew[2])
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute(selectByPublisherQuery)
    recordOfPublishers = cur.fetchall()
    cur.close()
    conn.commit()
    bookLabel = tkinter.Label(frame1, text="TITLE           AUTHOR           ISBN        GENRE           NUM SOLD           SOLD IN LAST MONTH")
    bookLabel.pack()
    for i in recordOfPublishers:
        selectByPublisherQuery = "select isbn, count(publisher) from book natural join bookOrder where isbn=%s group by publisher, isbn" %(i[2])
        conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
        getBooksSoldThisMonth(i[2])
        cur = conn.cursor()
        cur.execute(selectByPublisherQuery)
        numberSold = cur.fetchone()
        cur.close()
        conn.commit()
        if numberSold == None:
            labelStr = str(i[0]) + "     " + str(i[1]) +  "      " + str(i[2]) + "       " + str(i[3]) + "      0       0"
            bookLabel = tkinter.Label(frame1, text=labelStr)
            bookLabel.pack()
        else:
            labelStr = str(i[0]) + "     " + str(i[1]) +  "      " + str(i[2]) +   "       " + str(i[3]) + "      " + str(numberSold[1]) +  "       " + str(getBooksSoldThisMonth(i[2]))
            bookLabel = tkinter.Label(frame1, text=labelStr)
            bookLabel.pack()

def getBooksSoldThisMonth(isbn):
    now = str(datetime.now().strftime('%Y-%m-%d'))
    dateThen = str((datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))

    query = "select * from orderInfo natural join bookOrder natural join book where isbn=%s" %(isbn)
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute(query)
    recordOfPublishers = cur.fetchall()
    cur.close()
    numSold = 0
    for i in recordOfPublishers:
        if i[3] <= now and i[3] >= dateThen:
            numSold += 1
    return numSold

        

def loadOwnerFromMain(arg, userID):
    getUser = "select * from customer where user_id=%s" %(userID)
    conn = psycopg2.connect("dbname=Bookstore user=postgres password=postgres")
    cur = conn.cursor()
    cur.execute(getUser)
    recordNew = cur.fetchone()
    cur.close()
    conn.commit()
    clearScreen()
    frame1 = tkinter.Frame(root)
    frame1.pack()
    title23 = "Welcome back, Bookstore Owner %s" %(recordNew[1])
    t1= tkinter.Label(frame1, text=title23)
    t1.pack()
    addBook = tkinter.Button(frame1,text="Add Book Manually")
    addBook.bind('<Button-1>', lambda event: addBookManually(root,recordNew))
    addBook.pack()
    removeBook = tkinter.Button(frame1,text="Remove Book")
    removeBook.bind('<Button-1>', lambda event: removeBookManually(root,recordNew))
    removeBook.pack()
    displayPublisher = tkinter.Button(frame1,text="Display Publisher Reports")
    displayPublisher.bind('<Button-1>', lambda event: displayPublisherInfo(root,recordNew))
    displayPublisher.pack()

def ownerMainMenu(recordNew):
    clearScreen()
    frame1 = tkinter.Frame(root)
    frame1.pack()
    title23 = "Welcome back, Bookstore Owner %s" %(recordNew[1])
    t1= tkinter.Label(frame1, text=title23)
    t1.pack()
    addBook = tkinter.Button(frame1,text="Add Book Manually")
    addBook.bind('<Button-1>', lambda event: addBookManually(root,recordNew))
    addBook.pack()
    removeBook = tkinter.Button(frame1,text="Remove Book")
    removeBook.bind('<Button-1>', lambda event: removeBookManually(root,recordNew))
    removeBook.pack()
    displayPublisher = tkinter.Button(frame1,text="Display Publisher Reports")
    displayPublisher.bind('<Button-1>', lambda event: displayPublisherInfo(root,recordNew))
    displayPublisher.pack()



root = tkinter.Tk()
root.title('Web Interface')
root.geometry("500x550+0+0")
root.resizable(width=False, height=False)
frame1 = tkinter.Frame(root)
frame1.pack()

t = tkinter.Label(frame1, text="LOG-IN FOR USER SIDE")
t.pack()
w = tkinter.Label(frame1, text="User ID: ")
w.pack()
entry = tkinter.Entry(frame1)
entry.pack()
b = tkinter.Button(frame1,text="Enter")
b.bind('<Button-1>', loadUserFromMain)
b.pack()

t1 = tkinter.Label(frame1, text="LOG-IN FOR OWNER SIDE")
t1.pack()
w1 = tkinter.Label(frame1, text="Owner ID: ")
w1.pack()
b1 = tkinter.Button(frame1,text="Enter")
entry8 = tkinter.Entry(frame1)
entry8.pack()
b1.bind('<Button-1>', lambda event: loadOwnerFromMain(root, entry8.get()))
b1.pack()

b2 = tkinter.Button(frame1,text="Create New User")
b2.bind('<Button-1>', createNewUser)
b2.pack()

root.mainloop()