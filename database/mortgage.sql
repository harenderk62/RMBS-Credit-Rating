-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: mortgage_db
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `mortgages`
--

DROP TABLE IF EXISTS `mortgages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mortgages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `credit_score` int NOT NULL,
  `loan_amount` float NOT NULL,
  `property_value` float NOT NULL,
  `annual_income` float NOT NULL,
  `debt_amount` float NOT NULL,
  `loan_type` enum('fixed','adjustable') NOT NULL,
  `property_type` enum('single_family','condo') NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mortgages`
--

LOCK TABLES `mortgages` WRITE;
/*!40000 ALTER TABLE `mortgages` DISABLE KEYS */;
INSERT INTO `mortgages` VALUES (3,723,7613280,287638,8763,2736,'adjustable','condo','2025-04-10 16:57:56'),(4,726,4231,142312,23412,1243,'fixed','condo','2025-04-10 17:23:34'),(5,532,2134,234,234,234,'fixed','single_family','2025-04-10 17:35:44'),(6,234,1231,1231,312,13231,'fixed','single_family','2025-04-10 17:42:34'),(8,12,12123300,123,10,600,'adjustable','condo','2025-04-10 18:07:30'),(10,321,23112,123,321,123133,'fixed','condo','2025-04-10 18:16:11'),(11,111,11111,11,11123100,131312000,'fixed','condo','2025-04-10 18:17:16'),(13,600,300000,250000,40000,50000,'adjustable','condo','2025-04-10 18:55:08'),(14,300,100000,120000,30000,5000,'fixed','single_family','2025-04-10 18:55:08'),(15,750,200000,250000,60000,10000,'fixed','single_family','2025-04-10 18:55:46'),(16,600,300000,250000,40000,50000,'adjustable','condo','2025-04-10 18:55:46'),(17,300,100000,120000,30000,5000,'fixed','single_family','2025-04-10 18:55:46'),(18,750,200000,250000,60000,10000,'fixed','single_family','2025-04-10 18:58:30'),(19,600,300000,250000,40000,50000,'adjustable','condo','2025-04-10 18:58:31'),(20,300,100000,120000,30000,5000,'fixed','single_family','2025-04-10 18:58:31');
/*!40000 ALTER TABLE `mortgages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'mortgage_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-11  1:59:45
