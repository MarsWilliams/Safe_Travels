CREATE TABLE alternate_name (
    alternate_name_id int
    geoname_id int,
    iso_language varchar(7),
    alternate_name varchar(200),
    isPreferredName TINYINT,
    isShortName TINYINT,
    isColloquial TINYINT,
    isHistoric TINYINT,
    PRIMARY KEY (alternate_name_id)
);