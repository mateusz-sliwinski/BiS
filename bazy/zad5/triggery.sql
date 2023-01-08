CREATE TABLE department_archive(department_id INT, department_name VARCHAR(50), close_date DATE, last_manager VARCHAR(50));
DROP TABLE department_archive;
CREATE OR REPLACE TRIGGER add_to_archive AFTER DELETE ON departments
    FOR EACH ROW
    DECLARE
        PRAGMA AUTONOMOUS_TRANSACTION;
        v_manager_name VARCHAR(50); 
        v_first_name VARCHAR(50);
        v_last_name VARCHAR(50);
    BEGIN
        SELECT first_name, last_name INTO v_first_name, v_last_name
            FROM employees WHERE employee_id = :OLD.manager_id;
        v_manager_name := v_first_name || ' ' || v_last_name;
        INSERT INTO department_archive VALUES(:OLD.department_id, :OLD.department_name, CURRENT_DATE, v_manager_name);
        COMMIT;
    END;
    
DELETE FROM departments WHERE department_id = 50;


DROP TABLE thief;
CREATE TABLE thief (
   v_user varchar2(50),
   time_change timestamp
);

CREATE OR REPLACE PROCEDURE CheckSalary 
   (p_salary IN NUMBER) 
IS 
BEGIN 
   IF p_salary < 2000 OR p_salary > 26000 THEN 
      INSERT INTO thief (v_user, time_change) 
      VALUES (
         USER, 
         SYSDATE
      );
   END IF; 

END;

CREATE OR REPLACE TRIGGER CheckSalaryTrigger BEFORE INSERT OR UPDATE ON employees FOR EACH ROW
BEGIN 
   CheckSalary(:NEW.salary);
END; 
/

UPDATE employees SET salary = 200 WHERE employee_id = 102; 



CREATE SEQUENCE employees_seq START WITH 151 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER employees_trig
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
SELECT employees_seq.NEXTVAL
INTO :new.employee_id
FROM dual;
END;



CREATE OR REPLACE TRIGGER JOB_GRADES_TRIGGER 
BEFORE INSERT OR UPDATE OR DELETE ON JOB_GRADES 
FOR EACH ROW 
BEGIN 
RAISE_APPLICATION_ERROR(-20001, 'insert, update i delete s¹ banned na tabeli JOB_GRADES'); 
END;


CREATE OR REPLACE TRIGGER salary_trigger
BEFORE UPDATE ON jobs
FOR EACH ROW
BEGIN
  IF :NEW.min_salary != :OLD.min_salary OR :NEW.max_salary != :OLD.max_salary THEN
    RAISE_APPLICATION_ERROR (-20201, 'Cannot update min_salary or max_salary');
  END IF;
END;
/
