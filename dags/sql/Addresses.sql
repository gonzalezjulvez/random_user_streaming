CREATE TABLE IF NOT EXISTS addresses (
    id SERIAL PRIMARY KEY,
    person_id UUID REFERENCES persons(id),
    address TEXT,
    post_code VARCHAR(10)
);
