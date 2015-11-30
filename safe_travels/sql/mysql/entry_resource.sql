CREATE TABLE entry_resource (
    id INT NOT NULL AUTO_INCREMENT,
    entry_id INT,
    name VARCHAR(255),
    type VARCHAR(255),
    resource VARCHAR(255),
    PRIMARY KEY (id)
);