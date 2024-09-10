/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.4.21-MariaDB : Database - oss
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`oss` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `oss`;

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `id` int(200) unsigned NOT NULL AUTO_INCREMENT,
  `Productid` varchar(200) DEFAULT NULL,
  `Category` varchar(200) DEFAULT NULL,
  `feedback` varchar(200) DEFAULT NULL,
  `Useremail` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `feedback` */

insert  into `feedback`(`id`,`Productid`,`Category`,`feedback`,`Useremail`) values (1,'1','Suits','Good','mouli@gmail.com'),(2,'1','Suits','too bad','kumar@gmail.com');

/*Table structure for table `mycart` */

DROP TABLE IF EXISTS `mycart`;

CREATE TABLE `mycart` (
  `Id` int(200) unsigned NOT NULL AUTO_INCREMENT,
  `Categoryname` varchar(200) DEFAULT NULL,
  `ProductId` varchar(200) DEFAULT NULL,
  `Productname` varchar(200) DEFAULT NULL,
  `Productprice` varchar(200) DEFAULT NULL,
  `NoofItems` varchar(200) DEFAULT NULL,
  `TotalPrice` varchar(200) DEFAULT NULL,
  `Useremail` varchar(200) DEFAULT NULL,
  `Imagename` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT 'pending',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `mycart` */

insert  into `mycart`(`Id`,`Categoryname`,`ProductId`,`Productname`,`Productprice`,`NoofItems`,`TotalPrice`,`Useremail`,`Imagename`,`status`) values (1,'Suits','1','Tuxedo','25000','6','150000','mouli@gmail.com','tuxedo4.jpg','pending'),(2,'Suits','1','Tuxedo','25000','3','75000','mouli@gmail.com','tuxedo4.jpg','pending'),(3,'Suits','1','Tuxedo','25000','6','150000','mouli@gmail.com','tuxedo4.jpg','pending');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `id` int(200) unsigned NOT NULL AUTO_INCREMENT,
  `cardname` varchar(200) DEFAULT NULL,
  `cardnumber` varchar(200) DEFAULT NULL,
  `cardcvv` varchar(200) DEFAULT NULL,
  `carded` varchar(200) DEFAULT NULL,
  `useremail` varchar(200) DEFAULT NULL,
  `Expirydate` varchar(200) DEFAULT NULL,
  `Productname` varchar(200) DEFAULT NULL,
  `Productcount` varchar(200) DEFAULT NULL,
  `Totalprice` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

/*Data for the table `payment` */

insert  into `payment`(`id`,`cardname`,`cardnumber`,`cardcvv`,`carded`,`useremail`,`Expirydate`,`Productname`,`Productcount`,`Totalprice`) values (1,'KIRAN KUMAR KALLAM','9548542156','159','02/45','mouli@gmail.com','2022-08-16','Tuxedo','9','225000');

/*Table structure for table `productlist` */

DROP TABLE IF EXISTS `productlist`;

CREATE TABLE `productlist` (
  `ID` int(200) unsigned NOT NULL AUTO_INCREMENT,
  `ProductId` varchar(200) NOT NULL,
  `Category` varchar(200) NOT NULL,
  `ProductName` varchar(200) DEFAULT NULL,
  `ProductPrice` varchar(200) DEFAULT NULL,
  `ProductDescription` varchar(200) DEFAULT NULL,
  `ProductImage` varchar(200) DEFAULT NULL,
  `Path` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`ID`,`ProductId`,`Category`),
  UNIQUE KEY `ID` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Data for the table `productlist` */

insert  into `productlist`(`ID`,`ProductId`,`Category`,`ProductName`,`ProductPrice`,`ProductDescription`,`ProductImage`,`Path`) values (1,'1','Suits','Tuxedo','25000','classic,formal','tuxedo4.jpg','static/products/tuxedo4.jpg');

/*Table structure for table `userorder` */

DROP TABLE IF EXISTS `userorder`;

CREATE TABLE `userorder` (
  `ID` int(200) unsigned NOT NULL AUTO_INCREMENT,
  `ProductId` varchar(200) NOT NULL,
  `Category` varchar(200) NOT NULL,
  `ProductName` varchar(200) DEFAULT NULL,
  `ProductPrice` varchar(200) DEFAULT NULL,
  `ProductDescription` varchar(200) DEFAULT NULL,
  `ProductImage` varchar(200) DEFAULT NULL,
  `Useremail` varchar(200) DEFAULT NULL,
  `Productcount` int(200) unsigned DEFAULT NULL,
  `Totalprice` int(200) unsigned DEFAULT NULL,
  `status` varchar(200) DEFAULT 'pending',
  PRIMARY KEY (`ID`,`ProductId`,`Category`),
  UNIQUE KEY `ID` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

/*Data for the table `userorder` */

insert  into `userorder`(`ID`,`ProductId`,`Category`,`ProductName`,`ProductPrice`,`ProductDescription`,`ProductImage`,`Useremail`,`Productcount`,`Totalprice`,`status`) values (1,'1','Suits','Tuxedo','25000','classic,formal','tuxedo4.jpg','mouli@gmail.com',6,150000,'pending'),(8,'1','Suits','Tuxedo','25000','pending','tuxedo4.jpg','mouli@gmail.com',3,75000,'pending');

/*Table structure for table `userreg` */

DROP TABLE IF EXISTS `userreg`;

CREATE TABLE `userreg` (
  `Id` int(200) unsigned NOT NULL AUTO_INCREMENT,
  `Username` varchar(200) DEFAULT NULL,
  `Useremail` varchar(200) DEFAULT NULL,
  `Userage` varchar(200) DEFAULT NULL,
  `Usercontact` varchar(200) DEFAULT NULL,
  `Useraddress` varchar(200) DEFAULT NULL,
  `Userpassword` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `userreg` */

insert  into `userreg`(`Id`,`Username`,`Useremail`,`Userage`,`Usercontact`,`Useraddress`,`Userpassword`) values (1,'mouli','mouli@gmail.com','35','9848025645','chittor dist(kotthapalli )','Malli@123'),(2,'kumar','kumar@gmail.com','54','9848025645','chittor dist(kotthapalli )','Kumar@123');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
