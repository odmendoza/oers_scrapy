CREATE DATABASE `oerintegrationdb`; /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */

USE oerintegrationdb;

CREATE TABLE `cleantriple` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject_uri` text COLLATE utf8_bin,
  `predicate` text COLLATE utf8_bin,
  `object` text COLLATE utf8_bin,
  `subject_id` text COLLATE utf8_bin,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3922 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `triple` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject` text COLLATE utf8_bin,
  `predicate` text COLLATE utf8_bin,
  `object` text COLLATE utf8_bin,
  `source` text COLLATE utf8_bin,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13032 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


