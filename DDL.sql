create table address
	(address_id		integer,
	 streetNum		integer,
	 streetName		varchar(30),
	 city			varchar(20),
	 country		varchar(20),
	 postCode		varchar(20),
	 primary key (address_id)
	);

create table billingAddress
	(user_id		integer,
	 address_id	integer,
	 primary key (user_id),
	 foreign key (address_id) references address
	);

create table deliveryAddress
	(user_id		integer,
	 address_id	integer,
	 primary key (user_id),
	 foreign key (address_id) references address
	);

create table bankAccount
	(bankAccount_id		integer,
	 balance		integer,
	 primary key (bankAccount_id)
	);

create table bookPublisher
	(publisher_Name		varchar(30),
	 address_id		integer,
	 email			varchar(40),
	 phoneNum		varchar(15),
	 bankAccount_id		integer,
	 primary key (publisher_Name),
	 foreign key (address_id) references address,
	 foreign key (bankAccount_id) references bankAccount
	);

create table book
	(book_Name		varchar(50),
	 author_Name		varchar(40),
	 ISBN   		integer,
	 genre			varchar(10),
	 publisher_Name		varchar(30),
	 numPages		integer,
	 price			numeric(6,2),
	 quantity		integer,
	 primary key (ISBN),
	 foreign key (publisher_Name) references bookPublisher
	);

create table bookOrder
	(orderNum		integer, 
	 ISBN			integer,
	 primary key (orderNum, ISBN),
	 foreign key (ISBN) references book
	);

create table orderInfo
	(orderNum		integer,
	 trackingNum		integer,
	 orderDate		varchar(10),
	 primary key (orderNum)
	);

create table userOrder
	(user_id 		integer,
	 orderNum 		integer,
	 primary key (user_id, orderNum),
	 foreign key (orderNum) references orderInfo
	);

create table userBasket
	(user_id		integer,
	 ISBN			integer,
	 primary key (user_id, ISBN),
	 foreign key (ISBN) references book
	);

create table customer
	(user_id		integer, 
	 name 			varchar(50), 
	 billingAddress_id	integer,
	 deliveryAddress_id	integer,
	 primary key (user_id),
	 foreign key (billingAddress_id) references billingAddress,
	 foreign key (deliveryAddress_id) references deliveryAddress 
	)


