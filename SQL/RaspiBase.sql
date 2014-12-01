-- phpMyAdmin SQL Dump
-- version 3.5.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generato il: Mar 08, 2013 alle 10:51
-- Versione del server: 5.5.28-1
-- Versione PHP: 5.4.4-14

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE DATABASE `RaspiBase` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `RaspiBase`;


--
-- Database: `RaspiBase`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `pinDescription`
--

CREATE TABLE IF NOT EXISTS `pinDescription` (
  `pinID` int(11) NOT NULL AUTO_INCREMENT,
  `pinNumber` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `pinPos` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `pinDescription` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`pinID`),
  UNIQUE KEY `pinNumber` (`pinNumber`),
  UNIQUE KEY `pinPos` (`pinPos`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=9 ;

--
-- Dump dei dati per la tabella `pinDescription`
--

INSERT INTO `pinDescription` (`pinID`, `pinNumber`, `pinPos`, `pinDescription`) VALUES
(1, '4', '7', 'GPIO4'),
(2, '17', '11', 'GPIO17'),
(3, '18', '12', 'GPIO18'),
(4, '21', '13', 'GPIO21'),
(5, '22', '15', 'GPIO22'),
(6, '23', '16', 'GPIO23'),
(7, '24', '18', 'GPIO24'),
(8, '25', '22', 'GPIO25');

-- --------------------------------------------------------

--
-- Struttura della tabella `pinMsg`
--

CREATE TABLE IF NOT EXISTS `pinMsg` (
  `pinID` int(11) NOT NULL AUTO_INCREMENT,
  `pinNumber` varchar(2) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `pinMsgON` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `pinMsgOFF` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`pinID`),
  UNIQUE KEY `pinNumber` (`pinNumber`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dump dei dati per la tabella `pinMsg`
--

INSERT INTO `pinMsg` (`pinID`, `pinNumber`, `pinMsgON`, `pinMsgOFF`) VALUES
(3, '18', 'led aux acceso', 'led aux spento');

-- --------------------------------------------------------

--
-- Struttura della tabella `pinStatus`
--

CREATE TABLE IF NOT EXISTS `pinStatus` (
  `pinID` int(11) NOT NULL AUTO_INCREMENT,
  `pinNumber` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `pinDir` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  `pinStatus` varchar(1) COLLATE utf8_unicode_ci NOT NULL,
  `pinCms` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pinMod` varchar(1) COLLATE utf8_unicode_ci NOT NULL,
  `pinMess` varchar(1) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`pinID`),
  UNIQUE KEY `pinNumber` (`pinNumber`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=9 ;

--
-- Dump dei dati per la tabella `pinStatus`
--

INSERT INTO `pinStatus` (`pinID`, `pinNumber`, `pinDir`, `pinStatus`, `pinCms`, `pinMod`, `pinMess`) VALUES
(3, '18', 'out', '0', 'AUX_1', '1', '1'),
(6, '23', 'out', '1', 'COND_1', '1', '0'),
(7, '24', 'out', '0', 'RISC_1', '1', '0'),
(8, '25', 'out', '0', 'MESS_1', '1', '0');

-- --------------------------------------------------------

--
-- Struttura della tabella `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `userID` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(28) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `salt` varchar(8) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`userID`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=4 ;

--
-- Dump dei dati per la tabella `users`
--

INSERT INTO `users` (`userID`, `username`, `password`, `salt`) VALUES
(1, 'marco', '38c9e1392b3e1c92f413468e1f6b05292a1e7cd60824618ebca907952d19a43d', '9a8dac6d'),
(3, 'admin', '251034f22e2e96f7840efebbfd12c328a2263f6e324ddbff9ec865605ae12f09', '4a661889');

-- --------------------------------------------------------

--
-- Struttura della tabella `xMess`
--

CREATE TABLE IF NOT EXISTS `xMess` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `xMessID` varchar(2) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `xMess` varchar(200) DEFAULT NULL,
  `xMod` varchar(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `xMessID` (`xMessID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dump dei dati per la tabella `xMess`
--

INSERT INTO `xMess` (`ID`, `xMessID`, `xMess`, `xMod`) VALUES
(1, '1', '', '1');

-- --------------------------------------------------------

--
-- Struttura della tabella `xTemp`
--

CREATE TABLE IF NOT EXISTS `xTemp` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `xLocale` varchar(2) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `xMin` int(3) NOT NULL,
  `xMax` int(3) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `xLocale` (`xLocale`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dump dei dati per la tabella `xTemp`
--

INSERT INTO `xTemp` (`ID`, `xLocale`, `xMin`, `xMax`) VALUES
(1, '1', 24, 26);

