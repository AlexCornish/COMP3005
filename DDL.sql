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
	(customer_id		integer,
	 address_id		integer,
	 primary key (customer_id),
	 foreign key (address_id) references address
	);

create table deliveryAddress
	(customer_id		integer,
	 address_id	integer,
	 primary key (customer_id),
	 foreign key (address_id) references address
	);

create table product
	(product_id		integer,
	 product_name		varchar(50),
	 product_description	varchar(200),
	 price			numeric(10,2),
	 primary key (product_id)
	);
	
create table productAttribute
	(product_id		integer,
	 attribute_name		varchar(20),
	 attribute_info		varchar(100),
	 primary key (product_id, attribute_name),
	 foreign key (product_id) references product

create table orderItem
	(orderNum		integer, 
	 productID		integer,
	 primary key (orderNum, productID),
	 foreign key (productID) references product
	);

create table customer
	(customer_id		integer, 
	 name 			varchar(50), 
	 billingAddress_id	integer,
	 deliveryAddress_id	integer,
	 primary key (customer_id),
	 foreign key (billingAddress_id) references billingAddress,
	 foreign key (deliveryAddress_id) references deliveryAddress 
	)

create table customerOrder
	(orderNum		integer,
	 trackingNum		integer,
	 orderDate		varchar(10),                
	 orderTime 		varchar(10),
	 customer_id 		integer,
	 primary key (orderNum),
	 foreign key (customer_id) references customer
	);

create table customerBasket
	(user_id		integer,
	 product_id		integer,
	 primary key (user_id, product_id),
	 foreign key (product_id) references product
	);



