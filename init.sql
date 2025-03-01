CREATE TABLE IF NOT EXISTS mushrooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    edibility BOOLEAN NOT NULL,
    weight FLOAT NOT NULL,
    freshness INT NOT NULL
);

CREATE TABLE IF NOT EXISTS baskets (
    id SERIAL PRIMARY KEY,
    owner VARCHAR(255) NOT NULL,
    capacity INT NOT NULL
);

CREATE TABLE IF NOT EXISTS basket_mushrooms (
    basket_id INT REFERENCES baskets(id) ON DELETE CASCADE,
    mushroom_id INT REFERENCES mushrooms(id) ON DELETE CASCADE,
    PRIMARY KEY (basket_id, mushroom_id)
);