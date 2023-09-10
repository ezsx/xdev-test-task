-- Здесь можешь описать запросы для БД по созданию таблиц

drop table pillows;
drop table pillows_history;
drop table users;


--
-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(255),
--     email VARCHAR(255),
--     created_at TIMESTAMP NOT NULL,
--     updated_at TIMESTAMP
-- );

   CREATE TABLE pillows (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL, --REFERENCES users(id),
    device_uuid UUID,
    num_pillows INT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE TABLE pillows_history (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL, -- REFERENCES users(id),
    device_uuid UUID,
    amount INT NOT NULL,
    created_at TIMESTAMP NOT NULL
);

