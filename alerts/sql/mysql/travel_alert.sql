CREATE TABLE travel_alert (
    id INT NOT NULL AUTO_INCREMENT,
    feed_id INT,
    title VARCHAR(255),
    summary TEXT,
    published TIMESTAMP,
    subtitle text,
    created TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);