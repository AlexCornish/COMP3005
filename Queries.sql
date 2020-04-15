select max(address_id) from address
select max(user_id) from customer
"select * from customer where user_id=%d" %(idToCheck)
"select * from book where book_name='%s'" %(value)
"select * from book where author_name='%s'" %(value)
"select * from book where isbn=%d" %(value)
"select * from book where genre='%s'" %(value)
"select * from book natural join userBasket where user_id=%d" %(newRec[0][0])
"select sum(price) from book natural join userBasket where user_id=%d" %(newRec[0][0])
select max(ordernum) from orderInfo
select max(trackingnum) from orderInfo
"select * from book natural join userBasket where user_id=%d" %(user[0][0])

""" INSERT INTO orderInfo (ordernum, trackingnum, orderdate) VALUES (%s,%s,%s)"""
(orderID, trackingID, datetime.today().strftime('%Y-%m-%d'))

""" INSERT INTO userOrder(user_id, ordernum) VALUES (%s,%s)"""
(user[0][0], orderID)

"select ISBN from userBasket where user_id=%d" %(user[0][0])

""" INSERT INTO bookOrder(ordernum, isbn) VALUES (%s,%s)"""
(orderID,each)

"select sum(price) from book natural join userBasket where user_id=%d" %(user[0][0])
"update book set quantity = quantity - 1 where isbn = %d" %(individualBook[0])
"select * from book where quantity < 10 and isbn=%d" %(individualBook[0])
"update book set quantity = quantity + %d where isbn = %d" %(value, individualBook[0])
"select publisher, sum(0.25 * price) from book natural join userBasket group by publisher"
"select bankAccount_id from bookPublisher where name='%s'" %(i[0])
"update bankAccount set balance = balance + %f where bankaccount_id=%s" %(i[1],record3[0][0])
"delete from userBasket where user_id=%d" %(user[0][0])

" INSERT INTO userBasket (user_id, isbn) VALUES (%s,%s)"
(user[0][0], book[2])

"select * from book where isbn=%d" %(record[0])
"select * from userOrder natural join orderInfo where user_id=%d" %(newRec[0][0])
"select * from bookOrder natural join book where orderNum=%s" %(orderNum)

" INSERT INTO customer (user_id, name) VALUES (%s,%s)"
(userID, userName)

"INSERT INTO address (address_id, streetNum, streetName, city, country, postcode) VALUES (%s,%s,%s,%s,%s,%s)"
(billingAddress_id, billingAddressStreetNum, billingAddressStreetName, billingAddressCity, billingAddressCountry, billingAddressPostCode)

" INSERT INTO billingAddress (user_id, address_id) VALUES (%s,%s)"
(userID, billingAddress_id)

" INSERT INTO address (address_id, streetNum, streetName, city, country, postcode) VALUES (%s,%s,%s,%s,%s,%s)"
(deliveryAddress_id, deliveryAddressStreetNum, deliveryAddressStreetName, deliveryAddressCity, deliveryAddressCountry, deliveryAddresspostCode)

" INSERT INTO deliveryAddress (user_id, address_id) VALUES (%s,%s)"
(userID, deliveryAddress_id)

""" INSERT INTO book (book_Name, author_Name, ISBN, genre, publisher, numPages, price, quantity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
(name,author, ISBN, genre, publisher,numPages,price,quantity)

"delete from book where isbn=%s" %(ISBNToDelete)
"select * from bookPublisher"
"select * from bookPublisher natural join bankAccount natural join address where name='%s'" %(publisherInfo[0])
"select * from book where publisher='%s'" %(recordNew[2])
"select isbn, count(publisher) from book natural join bookOrder where isbn=%s group by publisher, isbn" %(i[2])
"select * from orderInfo natural join bookOrder natural join book where isbn=%s" %(isbn)
"select * from customer where user_id=%s" %(userID)
    
        
    
        
