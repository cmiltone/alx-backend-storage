-- script creates users table

DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255),
  name VARCHAR(255),
);
