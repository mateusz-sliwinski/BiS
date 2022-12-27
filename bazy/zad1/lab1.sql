CREATE TABLE REGIONS(
region_id int PRIMARY KEY NOT NULL,
region_name VARCHAR(45)
)

CREATE TABLE COUNTRIES(
country_id int PRIMARY KEY NOT NULL,
country_name VARCHAR(45)NOT NULL,
region_id int,
FOREIGN KEY (region_id) REFERENCES REGIONS(region_id) ON DELETE CASCADE
)

CREATE TABLE LOCATIONS(
location_id int PRIMARY KEY,
street_address VARCHAR(45),
postal_code VARCHAR(5),
city VARCHAR(200),
state_province VARCHAR(100),
country_id int,
FOREIGN KEY(country_id) REFERENCES COUNTRIES(country_id) ON DELETE CASCADE
)

CREATE TABLE DEPARTMENTS(
department_id int PRIMARY KEY,
departmemt_name VARCHAR(45),
manager_id int,
location_id int,
FOREIGN KEY (location_id) REFERENCES LOCATIONS(location_id) ON DELETE CASCADE
)


CREATE TABLE JOBS(
job_id int PRIMARY KEY,
job_tittle VARCHAR(100),
min_salary float, check (max_salary-min_salary>=2000),
max_salary float
)

CREATE TABLE EMPLOYEES (
employee_id int PRIMARY KEY,
first_name VARCHAR(245) NOT NULL,
last_name VARCHAR(245) NOT NULL,
email VARCHAR(150) NOT NULL check( 
    email Like '%@%.%' AND email NOT LIKE '@%' AND email NOT LIKE '%@%@%'
    ),
phone_number VARCHAR(12),
hire_date DATE NOT NULL,
job_id int,
FOREIGN KEY (job_id) REFERENCES JOBS(job_id) ON DELETE CASCADE,
salary float,
commision_pct VARCHAR(200),
manager_id int,
department_id int,
FOREIGN KEY (department_id) REFERENCES  DEPARTMENTS(department_id) ON DELETE CASCADE
)


ALTER TABLE EMPLOYEES ADD FOREIGN KEY(manager_id) REFERENCES EMPLOYEES(employee_id) ON DELETE CASCADE;

CREATE TABLE JOB_HISTORY(
employee_id int PRIMARY KEY,
FOREIGN KEY (employee_id) REFERENCES  EMPLOYEES(employee_id) ON DELETE CASCADE,
start_date DATE,
start_end DATE,
job_id int,
FOREIGN KEY (job_id) REFERENCES  JOBS(job_id) ON DELETE CASCADE,
department_id int,
FOREIGN KEY (department_id) REFERENCES  DEPARTMENTS(department_id) ON DELETE CASCADE
)



ALTER TABLE JOB_HISTORY DROP COLUMN start_end
ROLLBACK