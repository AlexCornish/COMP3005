# Gets the max address id from address, used in the creation of a new address id when 1 is added to it.
select max(address_id) from address

# Gets the max userid from customer used in the creation of a new user id when 1 is added to it.
select max(user_id) from customer

# Checks if a customer id is valid. 
"select * from customer where user_id=%d" %(idToCheck)

# Selects books that have the name "value"
"select * from book where book_name='%s'" %(value)

# Selects books with the author name "value"
"select * from book where author_name='%s'" %(value)

# Selects books with the ISBN value "value"
"select * from book where isbn=%d" %(value)

# Selects books that are in the genre of "value"
"select * from book where genre='%s'" %(value)

# Gets the contents of the user's basket and the book info of the books in the basket.
"select * from book natural join userBasket where user_id=%d" %(newRec[0][0])

# Calculates the price of all the books in the user's basket
"select sum(price) from book natural join userBasket where user_id=%d" %(newRec[0][0])

# Gets the max orderNum from orderInfo used in the creation of a new orderNum when 1 is added to it.
select max(ordernum) from orderInfo

# Gets the max trackingNum from orderInfo used in the creation of a new trackingNum when 1 is added to it.
select max(trackingnum) from orderInfo

# Inserts the order info into orderInfo
""" INSERT INTO orderInfo (ordernum, trackingnum, orderdate) VALUES (%s,%s,%s)"""
(orderID, trackingID, datetime.today().strftime('%Y-%m-%d'))

# Inserts the user order info into userOrder
""" INSERT INTO userOrder(user_id, ordernum) VALUES (%s,%s)"""
(user[0][0], orderID)

# Gets the ISBN numbers of the books in the user's basket.
"select ISBN from userBasket where user_id=%d" %(user[0][0])

# Inserts the book order info into bookOrder
""" INSERT INTO bookOrder(ordernum, isbn) VALUES (%s,%s)"""
(orderID,each)

# Updates the quantity of books when one is checked out
"update book set quantity = quantity - 1 where isbn = %d" %(individualBook[0])

# Gets the number of books that are under 10 in stock 
"select * from book where quantity < 10 and isbn=%d" %(individualBook[0])

# Updates the quantity of a book with the amount of it sold in the last month
"update book set quantity = quantity + %d where isbn = %d" %(value, individualBook[0])

# Gets the publisher and the amount of money they are owned from a user's basket during checkout
"select publisher, sum(0.25 * price) from book natural join userBasket group by publisher"

# Gets the publisher's bank account 
"select bankAccount_id from bookPublisher where name='%s'" %(i[0])

# Updates the publisher's bank account with the amount of money received from the user's basket
"update bankAccount set balance = balance + %f where bankaccount_id=%s" %(i[1],record3[0][0])

# Used to empty out the user's basket once the checkout procedure has finished.
"delete from userBasket where user_id=%d" %(user[0][0])

# Adds a book into a user basket by the creation of a userBasket object
" INSERT INTO userBasket (user_id, isbn) VALUES (%s,%s)"
(user[0][0], book[2])

# Gets the books ordered in book order based off of the orderNum
"select * from bookOrder natural join book where orderNum=%s" %(orderNum)

# Adding a new customer
" INSERT INTO customer (user_id, name) VALUES (%s,%s)"
(userID, userName)

# Adding a new address
"INSERT INTO address (address_id, streetNum, streetName, city, country, postcode) VALUES (%s,%s,%s,%s,%s,%s)"
(billingAddress_id, billingAddressStreetNum, billingAddressStreetName, billingAddressCity, billingAddressCountry, billingAddressPostCode)

# Adding a new billing address 
" INSERT INTO billingAddress (user_id, address_id) VALUES (%s,%s)"
(userID, billingAddress_id)

# Adding a new delivery address
" INSERT INTO deliveryAddress (user_id, address_id) VALUES (%s,%s)"
(userID, deliveryAddress_id)

# Used to add a new book to the database
""" INSERT INTO book (book_Name, author_Name, ISBN, genre, publisher, numPages, price, quantity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
(name,author, ISBN, genre, publisher,numPages,price,quantity)

# Used to delete a book from the system based on the ISBN 
"delete from book where isbn=%s" %(ISBNToDelete)

# Gets the list of book publishers
"select * from bookPublisher"


# Gets all the books published by a certain publisher
"select * from book where publisher='%s'" %(recordNew[2])

# Gets number of books sold by a publisher 
"select isbn, count(publisher) from book natural join bookOrder where isbn=%s group by publisher, isbn" %(i[2])

# Gets every instance of a certain book being ordered.
"select * from orderInfo natural join bookOrder natural join book where isbn=%s" %(isbn)