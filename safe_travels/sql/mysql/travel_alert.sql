CREATE TABLE travel_alert (
    id INT NOT NULL AUTO_INCREMENT,
    feed_id INT,
    country VARCHAR(255),
    title VARCHAR(255),
    summary TEXT,
    published TIMESTAMP,
    subtitle TEXT,
    created TIMESTAMP,
    PRIMARY KEY (id)
);