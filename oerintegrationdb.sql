CREATE DATABASE `oersdb`; /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */

USE oersdb;

CREATE TABLE `triplete` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject` text COLLATE utf8_bin,
  `predicate` text COLLATE utf8_bin,
  `object` text COLLATE utf8_bin,
  `repository` text COLLATE utf8_bin,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `crawl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject` text COLLATE utf8_bin,
  `predicate` text COLLATE utf8_bin,
  `object` text COLLATE utf8_bin,
  `source` text COLLATE utf8_bin,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

