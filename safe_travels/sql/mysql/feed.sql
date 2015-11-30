CREATE TABLE feed (
    id INT NOT NULL AUTO_INCREMENT,
    language VARCHAR(255),
    source VARCHAR(255),
    link VARCHAR(255),
    type VARCHAR(50),
    description TEXT,
    title VARCHAR(255),
    subtitle TEXT,
    created TIMESTAMP,
    PRIMARY KEY (id)
);