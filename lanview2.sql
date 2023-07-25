CREATE DATABASE lanview2;
USE lanview2;
CREATE TABLE hosts (
	id smallint unsigned not null auto_increment,
	status varchar(12),
	mac varchar(20),
	ip varchar(20),
	hostname varchar(32),
	vendor varchar(64),
	nickname varchar(32),
	first_seen int,
	last_seen int,
	visible int default 0,
	constraint pk_example primary key (id)
);
CREATE USER 'scanuser'@'localhost' IDENTIFIED BY 'KgXhP4ae';
CREATE USER 'phpuser'@'localhost' IDENTIFIED BY 'NYRrk2bG';
GRANT ALL ON lanview2.* TO 'scanuser'@'localhost';
GRANT SELECT on lanview2.* TO 'phpuser'@'localhost';
GRANT UPDATE (nickname) ON lanview2.hosts TO 'phpuser'@'localhost';
