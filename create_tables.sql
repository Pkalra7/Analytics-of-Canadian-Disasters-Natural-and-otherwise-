DROP TABLE if exists dimDate;

CREATE TABLE dimDate
(
	date_key SERIAL PRIMARY KEY,
	date_actual DATE NOT NULL,
	day_name VARCHAR(9) NOT NULL,
	month_name VARCHAR(9) NOT NULL,
	year_actual INT NOT NULL,
 	weekend BOOLEAN NOT NULL,
	season_Canada VARCHAR(7),
	season_International VARCHAR(7)
);

CREATE INDEX dimDate_date_actual_idx
	ON dimDate(date_actual);
	
DROP TABLE if exists dimDisaster;

CREATE TABLE dimDisaster
(
	disaster_key SERIAL PRIMARY KEY,
    disaster_type VARCHAR(40) NOT NULL,
	disaster_subgroup VARCHAR(40) NOT NULL,
	disaster_group	VARCHAR(20) NOT NULL,
	disaster_category VARCHAR(20) NOT NULL,
	magnitude INT,
	utility_people_affected INT
);

DROP TABLE if exists dimSummary;

CREATE TABLE dimSummary
(
	description_key SERIAL PRIMARY KEY,
	summary TEXT,
	keyword_one VARCHAR(20),
	keyword_two VARCHAR(20),
	keyword_three VARCHAR(20)
);

DROP TABLE if exists dimCosts;

CREATE TABLE dimCosts
(
	costs_key SERIAL PRIMARY KEY,
	estimated_total_cost NUMERIC(20,2),
	normalized_total_cost NUMERIC(20,2),
	federal_payments NUMERIC(20,2),
	provincial_payments NUMERIC(20,2),
    provincial_department_payments NUMERIC(20,2),
    municipal_costs NUMERIC(20,2),
    ogd_costs NUMERIC(20,2),
	insurance_payments NUMERIC(20,2),
    ngo_payments NUMERIC(20,2)
    
);

DROP TABLE if exists dimLocation;

CREATE TABLE dimLocation
(
	location_key SERIAL PRIMARY KEY,
	city VARCHAR(40) NOT NULL,
	province VARCHAR(30),
	country VARCHAR(30) NOT NULL,
	canada BOOLEAN NOT NULL
);

DROP TABLE if exists factCasualties;

CREATE TABLE factCasualties
(
	casualty_key SERIAL PRIMARY KEY,
	start_date_key INT NOT NULL,
	end_date_key INT NOT NULL,
	location_key INT NOT NULL,
	disaster_key INT NOT NULL,
	description_key INT NOT NULL,
	costs_key INT NOT NULL,
	fatalities INT,
	injured INT,
	evacuated INT
);

AlTER TABLE factCasualties ADD CONSTRAINT FK_start_date_key FOREIGN KEY (start_date_key)REFERENCES dimDate(date_key);

AlTER TABLE factCasualties ADD CONSTRAINT FK_end_date_key FOREIGN KEY (end_date_key)REFERENCES dimDate(date_key);

AlTER TABLE factCasualties ADD CONSTRAINT FK_location_key FOREIGN KEY (location_key)REFERENCES dimLocation(location_key);

AlTER TABLE factCasualties ADD CONSTRAINT FK_disaster_key FOREIGN KEY (disaster_key)REFERENCES dimDisaster(disaster_key);

AlTER TABLE factCasualties ADD CONSTRAINT FK_description_key FOREIGN KEY (description_key)REFERENCES dimSummary(description_key);

AlTER TABLE factCasualties ADD CONSTRAINT FK_costs_key FOREIGN KEY (costs_key)REFERENCES dimCosts(costs_key);