-- script creates a stored procedure AddBonus that adds a new correction for a student.
DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER $$
CREATE PROCEDURE AddBonus (user_id INT, project_name VARCHAR(255), score FLOAT)
BEGIN
    DECLARE total_projects INT DEFAULT 0;
    DECLARE project_id INT DEFAULT 0;

    SELECT COUNT(id)
        INTO total_projects
        FROM projects
        WHERE name = project_name;
    IF total_projects = 0 THEN
        INSERT INTO projects(name)
            VALUES(project_name);
    END IF;
    SELECT id
        INTO project_id
        FROM projects
        WHERE name = project_name;
    INSERT INTO corrections(user_id, project_id, score)
        VALUES (user_id, project_id, score);
END $$
DELIMITER ;