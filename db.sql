CREATE DATABASE IF NOT EXISTS rhdemo;
CREATE TABLE IF NOT EXISTS rhdemo.testtable (id INT AUTO_INCREMENT PRIMARY KEY, TKTKTK VARCHAR(255) NOT NULL);
INSERT INTO rhdemo.testtable (TKTKTK) VALUES ('tk111'), ('tktk2'), ('tk33333');
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER, CREATE TEMPORARY TABLES, CREATE VIEW, EVENT, TRIGGER, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, EXECUTE ON `rhdemo`.* TO 'flask'@'%';
