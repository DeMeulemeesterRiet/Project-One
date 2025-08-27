-- Demo schema (synthetic) and data for ProjectOne Riet
-- Alle data in dit script is synthetisch; geen secrets of persoonsgegevens.
CREATE DATABASE  IF NOT EXISTS `projectoneriet`; /* demo*/
USE `projectoneriet`;

--
-- Table structure for table `device`
--

CREATE TABLE `device` (
  `deviceid` int(11) NOT NULL AUTO_INCREMENT,
  `Naam` varchar(50) DEFAULT NULL,
  `Merk` varchar(50) DEFAULT NULL,
  `Beschrijving` varchar(100) DEFAULT NULL,
  `Meeteenheid` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`deviceid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
INSERT INTO `device` VALUES (1,'Temperatuursensor',NULL,NULL,'°C'),(2,'Afstandsensor',NULL,NULL,'BOOL');
UNLOCK TABLES;

--
-- Table structure for table `historiek`
--

CREATE TABLE `historiek` (
  `volgnummer` int(11) NOT NULL AUTO_INCREMENT,
  `deviceid` int(11) NOT NULL,
  `datumtijd` datetime DEFAULT NULL,
  `waarde` decimal(10,4) DEFAULT NULL,
  PRIMARY KEY (`volgnummer`),
  KEY `fk_toestel_idx` (`deviceid`),
  KEY `datumtijd_idx` (`datumtijd`),
  CONSTRAINT `fk_toestel` FOREIGN KEY (`deviceid`) REFERENCES `device` (`deviceid`)
) ENGINE=InnoDB AUTO_INCREMENT=391 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `ingeoefend`
--

CREATE TABLE `ingeoefend` (
  `Ingeoefendid` int(11) NOT NULL AUTO_INCREMENT,
  `oefensessieid` int(11) DEFAULT NULL,
  `tafelid` int(11) NOT NULL,
  `getal1` int(11) NOT NULL,
  `getal2` int(11) NOT NULL,
  `antwoord` int(11) DEFAULT NULL,
  `correct` bit(1) DEFAULT NULL,
  `registratiemoment` datetime DEFAULT NULL,
  PRIMARY KEY (`Ingeoefendid`),
  KEY `fk_oefensessie_idx` (`oefensessieid`),
  KEY `fk_tafel_idx` (`tafelid`),
  CONSTRAINT `fk_oefensessie` FOREIGN KEY (`oefensessieid`) REFERENCES `oefensessie` (`oefensessieid`),
  CONSTRAINT `fk_tafel` FOREIGN KEY (`tafelid`) REFERENCES `tafels` (`tafelid`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `leerlingen`
--
-- leerlingen (anoniem: geen plaintext wachtwoord/RFID)
CREATE TABLE `leerlingen` (
  `leerlingid` int(11) NOT NULL AUTO_INCREMENT,
  `naam` varchar(50) DEFAULT NULL,
  `password_hash` varchar(45) DEFAULT NULL,  -- demo placeholder, not a real hash
  `rfid_stub` varchar(45) DEFAULT NULL, -- demo stub, non-unique/optional
  PRIMARY KEY (`leerlingid`),
  UNIQUE KEY `rfidcode_UNIQUE` (`rfid_stub`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `oefensessie`
--

CREATE TABLE `oefensessie` (
  `oefensessieid` int(11) NOT NULL AUTO_INCREMENT,
  `leerlingid` int(11) NOT NULL,
  `startmoment` datetime DEFAULT NULL,
  `eindmoment` datetime DEFAULT NULL,
  PRIMARY KEY (`oefensessieid`),
  KEY `fk_gebruiker_idx` (`leerlingid`),
  CONSTRAINT `fk_gebruikerid` FOREIGN KEY (`leerlingid`) REFERENCES `leerlingen` (`leerlingid`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `tafels`
--

CREATE TABLE `tafels` (
  `tafelid` int(11) NOT NULL AUTO_INCREMENT,
  `Naam` varchar(45) DEFAULT NULL,
  `getal` int(11) NOT NULL,
  `Moeilijkheidsgraad` int(11) DEFAULT NULL,
  PRIMARY KEY (`tafelid`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tafels`
--

LOCK TABLES `tafels` WRITE;
INSERT INTO `tafels` VALUES (1,'Tafel 0',0,0),(2,'Tafel 1',1,1),(3,'Tafel 2',2,2),(4,'Tafel 3',3,5),(5,'Tafel 4',4,6),(6,'Tafel 5',5,4),(7,'Tafel 6',6,7),(8,'Tafel 7',7,8),(9,'Tafel 8',8,9),(10,'Tafel 9',9,10),(11,'Tafel 10',10,3),(12,'Tafel 11',11,11),(13,'Tafel 12',12,12),(14,'Tafel 13',13,13);
UNLOCK TABLES;

-- Dump completed on 2024-06-13 14:51:34
