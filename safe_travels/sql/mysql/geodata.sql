CREATE TABLE geodata (
    geoname_id INT,
    name VARCHAR(200),
    ascii_name VARCHAR(200),
    alternate_names VARCHAR(10000),
    latitude FLOAT(10, 6),
    longitude FLOAT(10, 6),
    feature_class CHAR(1),
    feature_code VARCHAR(10),
    country_code CHAR(2),
    cc2 VARCHAR(200),
    admin1_code VARCHAR(20)
    admin2_code VARCHAR(80)
    admin3_code VARCHAR(20)
    admin4_code VARCHAR(20)
    population bigint,
    elevation INT,
    dem INT,
    timezone  VARCHAR(40),
    modified DATE,
    created TIMESTAMP,
    PRIMARY KEY (geoname_id)
);