CREATE OR REPLACE FUNCTION name_job(v_job_id VARCHAR) RETURN VARCHAR IS
    v_job_title jobs.job_title%TYPE;
    BEGIN
        SELECT job_title INTO v_job_title FROM jobs WHERE job_id = v_job_id;
        RETURN v_job_title;
        EXCEPTION WHEN NO_DATA_FOUND THEN RETURN 'No data found';
    END name_job;
/
BEGIN
    DBMS_OUTPUT.PUT_LINE(name_job('DA_PRESWA'));
    DBMS_OUTPUT.PUT_LINE(name_job('AD_VP'));
END;
/
DROP FUNCTION name_job;

SET SERVEROUTPUT ON


CREATE OR REPLACE FUNCTION take_year_pay(v_employee_id IN NUMBER) RETURN NUMBER IS
    v_salary employees.salary%TYPE;
    BEGIN
    SELECT salary * (12 + commission_pct) INTO v_salary FROM EMPLOYEES WHERE employee_id = v_employee_id;
    RETURN v_salary;
    END take_year_pay; 

/
BEGIN
    DBMS_OUTPUT.PUT_LINE(take_year_pay(174));
END;
/


CREATE OR REPLACE FUNCTION take_prefix(phone_number VARCHAR2) RETURN VARCHAR2 IS
    prefix VARCHAR2(4);
    BEGIN
      SELECT SUBSTR(phone_number, 1, 3) INTO prefix FROM DUAL;
      RETURN prefix;
    END take_prefix;

/
BEGIN
    DBMS_OUTPUT.PUT_LINE(take_prefix('+48123456789'));
END;
/


CREATE OR REPLACE FUNCTION only_first_and_last(str IN VARCHAR2) RETURN VARCHAR2
IS
BEGIN
  RETURN INITCAP(SUBSTR(str, 1, 1)) || LOWER(SUBSTR(str, 2, LENGTH(str) - 2)) || UPPER(SUBSTR(str, LENGTH(str)));
END only_first_and_last; 

/
BEGIN
  DBMS_OUTPUT.PUT_LINE(only_first_and_last('HeLlo WoRld'));
END;
/