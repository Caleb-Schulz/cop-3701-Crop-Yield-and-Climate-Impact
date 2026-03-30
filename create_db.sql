CREATE TABLE crops (
  crop_id NUMBER PRIMARY KEY,
  crop_name VARCHAR2(100) NOT NULL,
);

CREATE TABLE locations (
  location_id NUMBER PRIMARY KEY,
  country VARCHAR2(100) NOT NULL,
);

CREATE TABLE yearly_conditions (
  condition_id NUMBER PRIMARY KEY,
  location_id NUMBER NOT NULL,
  year NUMBER NOT NULL,
  avg_rainfall FLOAT NOT NULL,
  avg_temp FLOAT NOT NULL,
  tonnes_pesticide FLOAT,

  CONSTRAINT fk_yc_location
    FOREIGN KEY (location_id)
    REFERENCES locations(location_id),

  CONSTRAINT unique_location_year
    UNIQUE (location_id, year)
);

CREATE TABLE yield_records (
  yield_id NUMBER PRIMARY KEY,
  crop_id NUMBER NOT NULL,
  location_id NUMBER NOT NULL,
  year NUMBER NOT NULL,
  hg_per_ha_yield FLOAT NOT NULL,

  CONSTRAINT fk_yield_crop
    FOREIGN KEY (crop_id)
    REFERENCES crops(crop_id),

  CONSTRAINT fk_yield_location
    FOREIGN KEY (location_id)
    REFERENCES locations(location_id),

  CONSTRAINT unique_crop_location_year
    UNIQUE (crop_id, location_id, year)
);
