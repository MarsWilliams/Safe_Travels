CREATE TABLE feed (
    id INT NOT NULL AUTO_INCREMENT,
    language_code VARCHAR(255),
    source VARCHAR(255),
    link VARCHAR(255),
    type VARCHAR(50),
    description TEXT,
    title VARCHAR(255),
    subtitle TEXT,
    created TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);