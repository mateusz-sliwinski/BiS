DECLARE
    numer_max NUMBER;
    nazwa departments.department_name%TYPE:='test';
BEGIN
    SELECT MAX(department_id) INTO numer_max FROM departments;
    DBMS_OUTPUT.PUT_LINE(numer_max);
    INSERT INTO departments (department_id, department_name)
        VALUES (numer_max + 10, nazwa);
END;

DECLARE
    numer_max NUMBER;
    nazwa departments.department_name%TYPE:='EDUCATION';
BEGIN
    SELECT MAX(department_id) INTO numer_max FROM departments;
    DBMS_OUTPUT.PUT_LINE(numer_max);
    INSERT INTO departments (department_id, department_name)
        VALUES (numer_max + 10, nazwa);
    UPDATE departments SET location_id = 3000
        WHERE department_id = numer_max + 10;
END;

CREATE TABLE nowa(pole VARCHAR(10));
BEGIN
    FOR i IN 1..10
    LOOP
        IF (i != 4 AND i != 6) 
        THEN INSERT INTO nowa(pole) VALUES(i);
        END IF;
    END LOOP;
END;

DECLARE
    panstwo countries%ROWTYPE;
BEGIN
    SELECT * INTO panstwo FROM countries WHERE country_id = 'CA';
    DBMS_OUTPUT.PUT_LINE('panstwo: ' || panstwo.country_name || ', id regionu: ' || panstwo.region_id);
END;

DECLARE
    TYPE dep_type IS TABLE OF
        departments.department_name%TYPE
        INDEX BY PLS_INTEGER;
    departamenty dep_type;
BEGIN
    FOR i IN 1..10
    LOOP
        SELECT department_name INTO departamenty(i) FROM departments
            WHERE department_id = 10 * i;
        DBMS_OUTPUT.PUT_LINE(departamenty(i));
    END LOOP;
END;

DECLARE
    TYPE dep_type IS TABLE OF
        departments%ROWTYPE
        INDEX BY PLS_INTEGER;
    departamenty dep_type;
BEGIN
    FOR i IN 1..10
    LOOP
        SELECT * INTO departamenty(i) FROM departments
            WHERE department_id = 10 * i;
        DBMS_OUTPUT.PUT_LINE(departamenty(i).department_id || ', ' || 
            departamenty(i).department_name || ', ' || 
            departamenty(i).manager_id || ', ' || 
            departamenty(i).location_id);
    END LOOP;
END;

DECLARE
    CURSOR salary_lastname_dept50 IS
        SELECT salary, last_name FROM employees WHERE department_id = 50;
    wiersz salary_lastname_dept50%ROWTYPE;
BEGIN
    OPEN salary_lastname_dept50;
    LOOP
        FETCH salary_lastname_dept50 INTO wiersz;
        EXIT WHEN salary_lastname_dept50%NOTFOUND;
        IF wiersz.salary > 3100 THEN
            DBMS_OUTPUT.PUT_LINE(wiersz.last_name || ' - nie dawaæ podwy¿ki');
        ELSE
            DBMS_OUTPUT.PUT_LINE(wiersz.last_name || ' - daæ podwy¿kê');
        END IF;
    END LOOP;
    CLOSE salary_lastname_dept50;
END;

DECLARE
    CURSOR dane(zarobki_min NUMBER, zarobki_max NUMBER, imie VARCHAR) IS
        SELECT salary, first_name, last_name FROM employees
        WHERE (salary BETWEEN zarobki_min AND zarobki_max)
        AND (LOWER(first_name) LIKE '%' || imie || '%');
    wiersz dane%ROWTYPE;
BEGIN
    FOR wiersz IN dane(1000, 5000, 'a')
    LOOP
        DBMS_OUTPUT.PUT_LINE(wiersz.salary || ', ' ||
            wiersz.first_name || ' ' || wiersz.last_name);
    END LOOP;
    FOR wiersz IN dane(5000, 20000, 'u')
    LOOP
        DBMS_OUTPUT.PUT_LINE(wiersz.salary || ', ' ||
            wiersz.first_name || ' ' || wiersz.last_name);
    END LOOP;
END;


CREATE OR REPLACE PROCEDURE dodaj_prace(V_ID IN VARCHAR, V_TITLE IN VARCHAR, V_MIN_SALARY IN INT, V_MAX_SALARY IN INT) IS 
    BEGIN
        INSERT INTO jobs VALUES (V_ID, V_TITLE,V_MIN_SALARY,V_MAX_SALARY);
        EXCEPTION
            WHEN OTHERS
            THEN DBMS_OUTPUT.PUT_LINE('ERORR NOT FOUND 404');
    END dodaj_prace;
/
BEGIN
    dodaj_prace('MSD_AST', 'SI developer', 3000,5000);
END;
/
CREATE TABLE error_log(user_name VARCHAR(20), error_number INT, error_msg VARCHAR(100));

create or replace PROCEDURE edytuj_opis(v_job_id_to_edit IN VARCHAR, v_Job_title_to_edit IN VARCHAR) IS
    no_jobs_updated EXCEPTION;
    error_number error_log.error_number%TYPE;
    error_info error_log.error_msg%TYPE;
    BEGIN
        UPDATE jobs SET jobs.JOB_TITLE = v_Job_title_to_edit WHERE jobs.JOB_ID = v_job_id_to_edit;
        IF SQL%NOTFOUND THEN RAISE no_jobs_updated;
        END IF;
        EXCEPTION
            WHEN no_jobs_updated THEN
            error_number := SQLCODE;
            error_info := SQLERRM;
            INSERT INTO error_log(user_name, error_number, error_msg) VALUES (USER, error_number, error_info);
    END edytuj_opis;
/
BEGIN
    edytuj_opis('lsd', 'error test');
END;
/

CREATE OR REPLACE PROCEDURE usun_prace(v_job_id_to_del IN VARCHAR) IS
    error_number error_log.error_number%TYPE;
    error_info error_log.error_msg%TYPE;
    no_jobs_deleted EXCEPTION;
    BEGIN
        DELETE FROM jobs WHERE jobs.job_id = v_job_id_to_del;
        IF SQL%NOTFOUND THEN RAISE no_jobs_deleted;
        END IF;
        EXCEPTION
            WHEN no_jobs_deleted THEN
            error_number := SQLCODE;
            error_info := SQLERRM;
            INSERT INTO error_log(user_name, error_number, error_msg)
            VALUES (USER, error_number, error_info);
    END usun_prace;
/
BEGIN
    usun_prace('MSD_AST');
    usun_prace('Paris Platynov');
END;
/


CREATE OR REPLACE PROCEDURE pokaz_zarobki(v_user_id IN NUMBER, v_name OUT VARCHAR, v_salary OUT NUMBER) IS
    BEGIN
        SELECT last_name, salary INTO v_name, v_salary FROM employees WHERE employee_id = v_user_id;
    END pokaz_zarobki;
    
/
DECLARE
    v_name employees.last_name%TYPE;
    v_salary employees.salary%TYPE;
    
BEGIN

    pokaz_zarobki(114, v_name, v_salary);
    DBMS_OUTPUT.PUT_LINE(v_name);
    DBMS_OUTPUT.PUT_LINE(v_salary);
    
END;
/

CREATE OR REPLACE PROCEDURE dodaj_pracownika(v_first_name IN VARCHAR, v_last_name IN VARCHAR,v_email IN VARCHAR, v_salary IN NUMBER) AS
    high_salary EXCEPTION;
    BEGIN
    IF v_salary <= 20000 THEN
    INSERT INTO employees(first_name, last_name, email, hire_date,job_id, salary, manager_id) 
    VALUES (v_first_name,v_last_name,v_email,'22/12/28','SA_MAN',v_salary,null);
    ELSE RAISE high_salary;
    END IF;
    EXCEPTION
        WHEN high_salary THEN
        INSERT INTO error_log(user_name, error_number, error_msg) VALUES (v_first_name, 2, 'salary is not correct');
    
    END dodaj_pracownika;
    
/
BEGIN
    dodaj_pracownika('Dawid','Jasper','dawid@jasper.com',5000);
    dodaj_pracownika('Natalia','Raczek','raczek@nieboraczek.pl',5000000);
    
END;
/