DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
	userId int NOT NULL AUTO_INCREMENT primary key,
    insertDate DATETIME null,
    name VARCHAR(255) not null, 
    address VARCHAR(255) not null, 
    address_latitude VARCHAR(255), 
    address_longitude VARCHAR(255), 
    phone VARCHAR(100) not null, 
    linkedin VARCHAR(100), 
    email VARCHAR(255) not null, 
    photo varchar(255),
    insightNotification bit DEFAULT 0, 
    status int DEFAULT 1, 
    currentCompany_Name VARCHAR(255), 
    currentCompany_latitude VARCHAR(255),
    currentCompany_longitude VARCHAR(255),
    oldCompany_Name VARCHAR(255),
    oldCompany_latitude VARCHAR(255),
    oldCompany_longitude VARCHAR(255),
    dataCompanyChanged DATETIME 
);

insert into customers (insertDate, name, address, phone, linkedin, email) values 
(now(), 'Pablo', 'Vila Mariana', '8978454787', 'https://www.linkedin.com/in/andre-iguodala-65b48ab5', 'pablosls@gmail.com'), 
(now(), 'Felipe', 'Vila Madalena', '54554454', 'https://www.linkedin.com/in/pablobrasil', 'fipele@gmail.com'), 
(now(), 'Ricardo', 'Paulista', '545554454', 'https://www.linkedin.com/in/pablobrasil', 'fipele@gmail.com'), 
(now(), 'Camila', 'Osasco', '545554454', 'https://www.linkedin.com/in/pablobrasil', 'camila@gmail.com'),
(now(), 'Renata', 'Guarulhos', '545554454', 'https://www.linkedin.com/in/pablobrasil', 'fipele@gmail.com'),
(now(), 'Juliana', 'Campinas', '545554454', 'https://www.linkedin.com/in/pablobrasil', 'juliana@gmail.com')
