CREATE TABLE IF NOT EXISTS contact_details (
    id SERIAL PRIMARY KEY,
    person_id UUID REFERENCES persons(id),
    email VARCHAR(100),
    username VARCHAR(50),
    phone VARCHAR(20),
    picture TEXT
);
