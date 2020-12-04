CREATE DATABASE Snakes_Ladders;

use Snakes_Ladders;

CREATE TABLE IF NOT EXISTS tblsnldImport
(`GameNumber` int AUTO_INCREMENT not null ,`GameLength` NUMERIC(5), PRIMARY KEY (`GameNumber`));

INSERT INTO tblsnldImport (GameNumber, GameLength) VALUES
    (1,30),
    (2,29),
    (3,31),
    (4,16),
    (5,24),
    (6,29),
    (7,28),
    (8,117),
    (9,42),
    (10,23);