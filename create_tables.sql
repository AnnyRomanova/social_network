CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    interests TEXT,
    city VARCHAR(50) NOT NULL,
    hashed_password VARCHAR(100) NOT NULL
);