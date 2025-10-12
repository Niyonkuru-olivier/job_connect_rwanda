-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: hireme
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (2,'oniyonkuru210@gmail.com','$2b$12$BI/5155kdQr8PRaRCPhy2uKnf2Zmf/bxaWRWEtDXMffDgZjFFvDAi','2025-10-07 18:13:00'),(3,'oniyonkuru@gmail.com','$2b$12$9khlR.8zp.BK.E8RzPUK6eODr5bBPx4RMx6vbfucbuEfpg8//c65y','2025-10-07 18:38:42');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `announcements`
--

DROP TABLE IF EXISTS `announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `announcements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcements`
--

LOCK TABLES `announcements` WRITE;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
INSERT INTO `announcements` VALUES (4,'Mantainance','Tomorrow we mantain our system from 1:00A.M-2:00A.M, means some features of our system are not working,\r\nbut after 2:00A.M all features are working again, Thank you for the patient','2025-10-10 10:52:31');
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `applications`
--

DROP TABLE IF EXISTS `applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `job_id` int NOT NULL,
  `status` enum('APPLIED','SHORTLISTED','REJECTED','HIRED') DEFAULT 'APPLIED',
  `cover_letter` varchar(255) DEFAULT NULL,
  `applied_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_app_user` (`user_id`),
  KEY `fk_app_job` (`job_id`),
  CONSTRAINT `fk_app_job` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_app_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applications`
--

LOCK TABLES `applications` WRITE;
/*!40000 ALTER TABLE `applications` DISABLE KEYS */;
INSERT INTO `applications` VALUES (1,7,2,'HIRED','hhhhhhhhhh','2025-10-07 14:09:35'),(3,2,4,'APPLIED','job','2025-10-08 06:02:15'),(4,1,4,'REJECTED','good','2025-10-08 06:03:15'),(5,7,4,'APPLIED','Dawidi_Admission_letter.pdf','2025-10-08 06:58:52'),(6,9,4,'APPLIED','Part_1.docx','2025-10-08 07:50:53'),(7,1,2,'APPLIED','certificateDoc1.docx','2025-10-08 09:44:44'),(8,10,5,'SHORTLISTED','certificateDoc1.docx','2025-10-09 13:47:42'),(9,2,2,'APPLIED','Part_1.docx','2025-10-10 08:32:17');
/*!40000 ALTER TABLE `applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `companies`
--

DROP TABLE IF EXISTS `companies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `companies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text,
  `website` varchar(255) DEFAULT NULL,
  `owner_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_companies_owner` (`owner_id`),
  CONSTRAINT `fk_companies_owner` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `companies`
--

LOCK TABLES `companies` WRITE;
/*!40000 ALTER TABLE `companies` DISABLE KEYS */;
INSERT INTO `companies` VALUES (1,'MTN Rwanda','We are Hiring a senior Software Developer','https://www.mtn.co.rw/',6,'2025-10-07 09:13:35','2025-10-07 11:13:35'),(3,'MININFRA','Ministry of Infrastructure','https://www.mininfra.gov.rw/',8,'2025-10-08 05:58:51','2025-10-08 06:08:36'),(4,'GOICO LTD','Is the market that located in Musanze city','www.GOICO.rw',11,'2025-10-09 13:31:42','2025-10-09 13:31:42');
/*!40000 ALTER TABLE `companies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_documents`
--

DROP TABLE IF EXISTS `employee_documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_documents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `file_name` varchar(255) DEFAULT NULL,
  `file_path` varchar(255) DEFAULT NULL,
  `file_type` enum('CV','DIPLOMA','CERTIFICATE') DEFAULT NULL,
  `uploaded_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_documents_user` (`user_id`),
  CONSTRAINT `fk_documents_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_documents`
--

LOCK TABLES `employee_documents` WRITE;
/*!40000 ALTER TABLE `employee_documents` DISABLE KEYS */;
INSERT INTO `employee_documents` VALUES (1,1,'farmer_users.pdf','static/uploads\\farmer_users.pdf','CERTIFICATE','2025-10-07 12:21:04'),(2,7,'UR-logo.png','static/uploads\\UR-logo.png','CV','2025-10-07 16:54:43'),(3,10,'HireMe_Rwanda.docx','static/uploads\\HireMe_Rwanda.docx','CV','2025-10-09 15:42:25'),(4,2,'Recommendation_Letter.docx','static/uploads\\Recommendation_Letter.docx','DIPLOMA','2025-10-10 10:33:05');
/*!40000 ALTER TABLE `employee_documents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_profiles`
--

DROP TABLE IF EXISTS `employee_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_profiles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `education` text,
  `skills` text,
  `experience` text,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_employee_user` (`user_id`),
  CONSTRAINT `fk_employee_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_profiles`
--

LOCK TABLES `employee_profiles` WRITE;
/*!40000 ALTER TABLE `employee_profiles` DISABLE KEYS */;
INSERT INTO `employee_profiles` VALUES (1,7,'+250781429742','Musanze','Bachelor degree','Software Development','2 years','2025-10-07 16:12:42'),(2,2,'+250781429744','Gicumbi','Bachelor\'s degree in Software Engineering','web Development','+5 years','2025-10-10 10:32:41'),(3,10,'+250780075414','Musanze-Rwanda','Bachelor degree in statistics','computer based skills, sports','+2 years as staticians','2025-10-09 15:41:46');
/*!40000 ALTER TABLE `employee_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `requirements` text,
  `location` varchar(255) DEFAULT NULL,
  `salary` varchar(100) DEFAULT NULL,
  `type` enum('FULL_TIME','PART_TIME','CONTRACT','INTERNSHIP') DEFAULT 'FULL_TIME',
  `deadline` datetime DEFAULT NULL,
  `company_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_jobs_company` (`company_id`),
  CONSTRAINT `fk_jobs_company` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (2,'Senior Software Developer','We are Hiring Software Developer','Bachelor Degree in Software Engineering and Related Fields','Kigali','1M','FULL_TIME','2025-10-23 00:00:00',1,'2025-10-07 09:21:12','2025-10-07 09:21:12'),(4,'Database Engineer','database Engineer have the responsibility to Mantains all activities of database used in the insititutions','Master\'s Degree','Kigali','2M','FULL_TIME','2025-10-20 00:00:00',3,'2025-10-08 06:01:14','2025-10-08 06:01:14'),(5,'Data Analyst','he/she can have the responsibility for collecting data','Holding a Bachelor degree in Statistics, Mathematics and related field','Musanze','400K','FULL_TIME','2025-10-25 00:00:00',4,'2025-10-09 13:34:30','2025-10-09 13:34:30');
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `national_id` char(16) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` enum('EMPLOYEE','EMPLOYER') NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `national_id` (`national_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Olivier Niyonkuru','1234567890123456','oniyonkuru233@gmail.com','EMPLOYEE','$2b$10$eb0PSwyYeonF3RQ4ALky7eqStXJNUfjGeddoRd4muGV0CMMB3NUgy','2025-10-03 17:11:40'),(2,'Jacques Tina','1234567890123459','oniyonkuru1@gmail.com','EMPLOYEE','$2b$10$ljKbnEIkLIRpK0RDGOw9VutwQklE9msLGAw391IpRUHN3Rp4DBDZm','2025-10-04 11:59:43'),(5,'John Doe','1234567890123100','employer@example.com','EMPLOYER','$2b$10$ri2hAl6.bg7DD1ycdInz9uYv/lijxMW8yr4CEqCeSonTIvSoGkgpa','2025-10-06 16:43:39'),(6,'Rwiza Alex','1234567891234567','habufitejames@mininfra.gov.rw','EMPLOYER','$2b$10$GgzazHJzItHnmnxiHOsArutCRTTft0whqc3UY63j3xEsxMKjnXvDa','2025-10-06 18:22:47'),(7,'Jacques Nziza','1200211234567890','joy120@gmail.com','EMPLOYEE','$2b$12$Y9lYkJt6Igaw1ObGbo4pyuX6KEzVpo7OSuCvSixt.MLcSWItSUuFa','2025-10-07 08:32:29'),(8,'Ashula Ishimwe','1200211234567820','ashula@gmail.com','EMPLOYER','$2b$12$Emhw5GmYc4.4q4cL21/0BuRHEVIKafP8rDKqTqE65US1IFIopPQSy','2025-10-08 05:56:25'),(9,'Arnaud Ishimwe','1200211234567810','arno@gmail.com','EMPLOYEE','$2b$12$lPLfXN0JqtdlkAA6e3G65.rJMGg.6AmO4fO0tHzQZpSQhF/hUNixi','2025-10-08 07:50:14'),(10,'Placide Gororerwa','1200211234567800','gororerwaplacide12@gmail.com','EMPLOYEE','$2b$12$szCX4Rv.T01LLu9kXUJR9.LkTiihnSkIIcDL4EMllvPJ2s5AqPAlO','2025-10-09 13:26:18'),(11,'James Iraguha','1234567890123455','iraguhajames20@gmail.com','EMPLOYER','$2b$12$pl2oPZCX3kd0FVRmG6LBSecZE.Ii6NT9B4S6Har93R1M2M2TxRYIu','2025-10-09 13:28:01');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-12 18:48:02
