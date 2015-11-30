CREATE TABLE feed (
    id INT NOT NULL AUTO_INCREMENT,
    metadata_id INT,
    language VARCHAR(255),
    source VARCHAR(255),
    link VARCHAR(255),
    type VARCHAR(50),
    description TEXT,
    title VARCHAR(255),
    subtitle TEXT,
    modified DATE,
    created TIMESTAMP,
    PRIMARY KEY (id)
);