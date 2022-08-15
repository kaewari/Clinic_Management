-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: btl
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guest_id` int NOT NULL,
  `phone_number` float NOT NULL,
  `created_date` datetime NOT NULL,
  `ID_card` float DEFAULT NULL,
  PRIMARY KEY (`id`,`guest_id`),
  KEY `guest_id` (`guest_id`),
  CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`guest_id`) REFERENCES `guest` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cashier`
--

DROP TABLE IF EXISTS `cashier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cashier` (
  `user_id` int NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `cashier_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cashier`
--

LOCK TABLES `cashier` WRITE;
/*!40000 ALTER TABLE `cashier` DISABLE KEYS */;
/*!40000 ALTER TABLE `cashier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Thuốc giảm đâu, hạ sốt'),(2,'Thuốc giải độc'),(3,'Thuốc kháng sinh'),(4,'Thuốc từ thiên'),(5,'Thuốc dị ứng'),(6,'Thuốc gây tê, mê'),(7,'Thuốc điều trị ký sinh trùng'),(8,'Thuốc tim mạch');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chi_tiet_toa_thuoc`
--

DROP TABLE IF EXISTS `chi_tiet_toa_thuoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chi_tiet_toa_thuoc` (
  `toathuoc_id` int NOT NULL,
  `medicine_id` int NOT NULL,
  `quantity` int DEFAULT NULL,
  `how_to_use` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`toathuoc_id`,`medicine_id`),
  KEY `medicine_id` (`medicine_id`),
  CONSTRAINT `chi_tiet_toa_thuoc_ibfk_1` FOREIGN KEY (`toathuoc_id`) REFERENCES `toathuoc` (`id`),
  CONSTRAINT `chi_tiet_toa_thuoc_ibfk_2` FOREIGN KEY (`medicine_id`) REFERENCES `medicine` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chi_tiet_toa_thuoc`
--

LOCK TABLES `chi_tiet_toa_thuoc` WRITE;
/*!40000 ALTER TABLE `chi_tiet_toa_thuoc` DISABLE KEYS */;
INSERT INTO `chi_tiet_toa_thuoc` VALUES (1,1,2,'uống'),(1,2,2,'uống'),(1,3,2,'uống'),(1,4,2,'uống'),(2,2,1,'asd'),(3,2,4,'adasd');
/*!40000 ALTER TABLE `chi_tiet_toa_thuoc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `city` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city`
--

LOCK TABLES `city` WRITE;
/*!40000 ALTER TABLE `city` DISABLE KEYS */;
/*!40000 ALTER TABLE `city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `danhsachkham`
--

DROP TABLE IF EXISTS `danhsachkham`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `danhsachkham` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nurse_id` int NOT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `nurse_id` (`nurse_id`),
  CONSTRAINT `danhsachkham_ibfk_1` FOREIGN KEY (`nurse_id`) REFERENCES `nurse` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `danhsachkham`
--

LOCK TABLES `danhsachkham` WRITE;
/*!40000 ALTER TABLE `danhsachkham` DISABLE KEYS */;
/*!40000 ALTER TABLE `danhsachkham` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `district`
--

DROP TABLE IF EXISTS `district`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `district` (
  `id` int NOT NULL AUTO_INCREMENT,
  `city_id` int NOT NULL,
  `name` varchar(50) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`,`city_id`),
  KEY `city_id` (`city_id`),
  CONSTRAINT `district_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `city` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `district`
--

LOCK TABLES `district` WRITE;
/*!40000 ALTER TABLE `district` DISABLE KEYS */;
/*!40000 ALTER TABLE `district` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor` (
  `user_id` int NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `doctor_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor`
--

LOCK TABLES `doctor` WRITE;
/*!40000 ALTER TABLE `doctor` DISABLE KEYS */;
INSERT INTO `doctor` VALUES (6);
/*!40000 ALTER TABLE `doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guest`
--

DROP TABLE IF EXISTS `guest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guest` (
  `user_id` int NOT NULL,
  `last_visited` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `guest_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guest`
--

LOCK TABLES `guest` WRITE;
/*!40000 ALTER TABLE `guest` DISABLE KEYS */;
INSERT INTO `guest` VALUES (7,NULL);
/*!40000 ALTER TABLE `guest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guest__danh_sach`
--

DROP TABLE IF EXISTS `guest__danh_sach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guest__danh_sach` (
  `guest_id` int NOT NULL,
  `danhsachkham_id` int NOT NULL,
  PRIMARY KEY (`guest_id`,`danhsachkham_id`),
  KEY `danhsachkham_id` (`danhsachkham_id`),
  CONSTRAINT `guest__danh_sach_ibfk_1` FOREIGN KEY (`guest_id`) REFERENCES `guest` (`user_id`),
  CONSTRAINT `guest__danh_sach_ibfk_2` FOREIGN KEY (`danhsachkham_id`) REFERENCES `danhsachkham` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guest__danh_sach`
--

LOCK TABLES `guest__danh_sach` WRITE;
/*!40000 ALTER TABLE `guest__danh_sach` DISABLE KEYS */;
/*!40000 ALTER TABLE `guest__danh_sach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager`
--

DROP TABLE IF EXISTS `manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager` (
  `user_id` int NOT NULL,
  `is_supervisor` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `manager_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager`
--

LOCK TABLES `manager` WRITE;
/*!40000 ALTER TABLE `manager` DISABLE KEYS */;
INSERT INTO `manager` VALUES (2,NULL);
/*!40000 ALTER TABLE `manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicine`
--

DROP TABLE IF EXISTS `medicine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicine` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `price` int NOT NULL,
  `image` varchar(100) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `unit` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
  `created_date` datetime DEFAULT NULL,
  `category_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `medicine_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicine`
--

LOCK TABLES `medicine` WRITE;
/*!40000 ALTER TABLE `medicine` DISABLE KEYS */;
INSERT INTO `medicine` VALUES (1,'Panadol','Thuốc giảm đau, hạ sốt',20000,'images/Thuốc giảm đau, hạ sốt/panadol.jpg',1,'Vien','2022-08-15 19:46:39',1),(2,'loratadin','Thuốc chống dị ứng',100000,'images/Thuốc chống dị ứng/loratadin.jpg',1,'Vien','2022-08-15 19:46:39',4),(3,'deferoxamin','Thuốc giải độc',50000,'images/Thuốc giải độc/deferoxamin.jpg',1,'Vien','2022-08-15 19:46:39',2),(4,'penicillin','Thuốc kháng sinh',50000,'images/Thuốc kháng sinh/penicillin.jpg',1,'Vien','2022-08-15 19:46:39',3),(5,'aloe vera','Thuốc từ thiên nhiên',50000,'images/Thuốc từ thiên nhiên/aloe vera.jpg',1,'Vien','2022-08-15 19:46:39',3);
/*!40000 ALTER TABLE `medicine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nurse`
--

DROP TABLE IF EXISTS `nurse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nurse` (
  `user_id` int NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `nurse_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nurse`
--

LOCK TABLES `nurse` WRITE;
/*!40000 ALTER TABLE `nurse` DISABLE KEYS */;
/*!40000 ALTER TABLE `nurse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phieukham`
--

DROP TABLE IF EXISTS `phieukham`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phieukham` (
  `id` int NOT NULL AUTO_INCREMENT,
  `doctor_id` int NOT NULL,
  `guest_id` int NOT NULL,
  `created_date` datetime DEFAULT NULL,
  `symptom` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
  `diagnose_disease` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`id`,`doctor_id`,`guest_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `guest_id` (`guest_id`),
  CONSTRAINT `phieukham_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`user_id`),
  CONSTRAINT `phieukham_ibfk_2` FOREIGN KEY (`guest_id`) REFERENCES `guest` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phieukham`
--

LOCK TABLES `phieukham` WRITE;
/*!40000 ALTER TABLE `phieukham` DISABLE KEYS */;
INSERT INTO `phieukham` VALUES (2,6,7,'2022-08-15 20:45:42','ho','ho'),(7,6,7,'2022-08-15 21:28:24','ads','asd'),(19,6,7,'2022-08-15 21:39:39','dasd','asd');
/*!40000 ALTER TABLE `phieukham` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receipt`
--

DROP TABLE IF EXISTS `receipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receipt` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cashier_id` int NOT NULL,
  `guest_id` int NOT NULL,
  `toathuoc_id` int NOT NULL,
  `created_date` datetime DEFAULT NULL,
  `medical_expense` int NOT NULL,
  PRIMARY KEY (`id`,`cashier_id`,`guest_id`,`toathuoc_id`),
  UNIQUE KEY `toathuoc_id` (`toathuoc_id`),
  KEY `cashier_id` (`cashier_id`),
  KEY `guest_id` (`guest_id`),
  CONSTRAINT `receipt_ibfk_1` FOREIGN KEY (`cashier_id`) REFERENCES `cashier` (`user_id`),
  CONSTRAINT `receipt_ibfk_2` FOREIGN KEY (`guest_id`) REFERENCES `guest` (`user_id`),
  CONSTRAINT `receipt_ibfk_3` FOREIGN KEY (`toathuoc_id`) REFERENCES `toathuoc` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receipt`
--

LOCK TABLES `receipt` WRITE;
/*!40000 ALTER TABLE `receipt` DISABLE KEYS */;
/*!40000 ALTER TABLE `receipt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receipt_detail`
--

DROP TABLE IF EXISTS `receipt_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receipt_detail` (
  `receipt_id` int NOT NULL,
  `medicine_id` int NOT NULL,
  `quantity` int DEFAULT NULL,
  `unit_price` int DEFAULT NULL,
  PRIMARY KEY (`receipt_id`,`medicine_id`),
  KEY `medicine_id` (`medicine_id`),
  CONSTRAINT `receipt_detail_ibfk_1` FOREIGN KEY (`receipt_id`) REFERENCES `receipt` (`id`),
  CONSTRAINT `receipt_detail_ibfk_2` FOREIGN KEY (`medicine_id`) REFERENCES `medicine` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receipt_detail`
--

LOCK TABLES `receipt_detail` WRITE;
/*!40000 ALTER TABLE `receipt_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `receipt_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rule`
--

DROP TABLE IF EXISTS `rule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `manager_id` int NOT NULL,
  `medical_expense` int NOT NULL,
  `patient` int NOT NULL,
  PRIMARY KEY (`id`,`manager_id`),
  KEY `manager_id` (`manager_id`),
  CONSTRAINT `rule_ibfk_1` FOREIGN KEY (`manager_id`) REFERENCES `manager` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rule`
--

LOCK TABLES `rule` WRITE;
/*!40000 ALTER TABLE `rule` DISABLE KEYS */;
/*!40000 ALTER TABLE `rule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `toathuoc`
--

DROP TABLE IF EXISTS `toathuoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `toathuoc` (
  `id` int NOT NULL AUTO_INCREMENT,
  `doctor_id` int NOT NULL,
  `guest_id` int NOT NULL,
  `phieukham_id` int NOT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`,`doctor_id`,`guest_id`),
  UNIQUE KEY `phieukham_id` (`phieukham_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `guest_id` (`guest_id`),
  CONSTRAINT `toathuoc_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`user_id`),
  CONSTRAINT `toathuoc_ibfk_2` FOREIGN KEY (`guest_id`) REFERENCES `guest` (`user_id`),
  CONSTRAINT `toathuoc_ibfk_3` FOREIGN KEY (`phieukham_id`) REFERENCES `phieukham` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `toathuoc`
--

LOCK TABLES `toathuoc` WRITE;
/*!40000 ALTER TABLE `toathuoc` DISABLE KEYS */;
INSERT INTO `toathuoc` VALUES (1,6,7,2,'2022-08-15 20:45:42'),(2,6,7,7,'2022-08-15 21:28:24'),(3,6,7,19,'2022-08-15 21:39:39');
/*!40000 ALTER TABLE `toathuoc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
  `username` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
  `password` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
  `joined_date` datetime DEFAULT NULL,
  `avatar` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `date_of_birth` datetime NOT NULL,
  `gender` enum('MALE','FEMALE','OTHERS') COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `address` varchar(50) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `user_role` enum('ADMIN','EMPLOYEE','USER') COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `city_id` int DEFAULT NULL,
  `district_id` int DEFAULT NULL,
  `ward_id` int DEFAULT NULL,
  `user_position` enum('DOCTOR','NURSE','MANAGER','CASHIER') COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `city_id` (`city_id`),
  KEY `district_id` (`district_id`),
  KEY `ward_id` (`ward_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `city` (`id`),
  CONSTRAINT `user_ibfk_2` FOREIGN KEY (`district_id`) REFERENCES `district` (`id`),
  CONSTRAINT `user_ibfk_3` FOREIGN KEY (`ward_id`) REFERENCES `ward` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (2,'admin','admin1','202cb962ac59075b964b07152d234b70',0,'admin1@gmail.com','2022-08-15 19:54:33','https://res.cloudinary.com/dt8p4xhzz/image/upload/v1660560772/images/Employee%20Pic/Doctor/tran-quang-binh-avt_dubfl8.png','2001-01-12 00:00:00','MALE',NULL,'ADMIN',NULL,NULL,NULL,'MANAGER'),(6,'admin','admin2','202cb962ac59075b964b07152d234b70',1,'admin2@gmail.com','2022-08-15 20:30:48','https://res.cloudinary.com/dt8p4xhzz/image/upload/v1660560772/images/Employee%20Pic/Doctor/tran-quang-binh-avt_dubfl8.png','2022-08-15 20:31:00','MALE',NULL,'EMPLOYEE',NULL,NULL,NULL,'DOCTOR'),(7,'Hoàng Thanh Sơn','HTS1','202cb962ac59075b964b07152d234b70',0,'sonhoang236@gmail.com','2022-08-15 20:30:48','https://res.cloudinary.com/dt8p4xhzz/image/upload/v1660571002/wehrx1khrmtpu0kdjsro.jpg','2001-03-26 00:00:00','MALE',NULL,'USER',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ward`
--

DROP TABLE IF EXISTS `ward`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ward` (
  `id` int NOT NULL AUTO_INCREMENT,
  `district_id` int NOT NULL,
  `name` varchar(50) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`,`district_id`),
  KEY `district_id` (`district_id`),
  CONSTRAINT `ward_ibfk_1` FOREIGN KEY (`district_id`) REFERENCES `district` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ward`
--

LOCK TABLES `ward` WRITE;
/*!40000 ALTER TABLE `ward` DISABLE KEYS */;
/*!40000 ALTER TABLE `ward` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-15 22:22:14
