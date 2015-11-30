CREATE TABLE entry_resource (
    id INT NOT NULL AUTO_INCREMENT,
    entry_id INT,
    name varchar(255),
    type varchar(255),
    resource varchar(255),
    PRIMARY KEY (id)
);