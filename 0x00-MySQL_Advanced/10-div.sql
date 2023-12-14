-- script creates a function SafeDiv that divides (and returns) the first by the second number or returns 0 if the second number is equal to 0.
DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER $$
CREATE FUNCTION SafeDiv (a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
  DECLARE return_val FLOAT DEFAULT 0;
  IF b != 0 THEN
    SET return_val = a / b;
  END IF;
  RETURN return_val;
END $$
DELIMITER ;
