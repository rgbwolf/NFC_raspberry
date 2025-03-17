CREATE DATABASE kasse;
 
USE kasse;
 
CREATE TABLE kundendaten (
    name VARCHAR(45),
    chip_id VARCHAR(45),
    PRIMARY KEY (chip_id)
);
 
CREATE TABLE Geldbetrag (
    chip_id VARCHAR(45),
    kontostand INT,
    PRIMARY KEY (chip_id),
    FOREIGN KEY (chip_id) REFERENCES kundendaten(chip_id)
);
