CREATE TABLE IF NOT EXISTS persons (
    id UUID PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(10),
    dob TIMESTAMP,
    registered_date TIMESTAMP
);
