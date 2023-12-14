-- script creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    ALTER TABLE users ADD weight_total INT NOT NULL;
    ALTER TABLE users ADD total_score_weighted INT NOT NULL;

    UPDATE users
        SET total_score_weighted = (
            SELECT SUM(corrections.score * projects.weight)
            FROM corrections
                INNER JOIN projects
                    ON corrections.project_id = projects.id
            WHERE corrections.user_id = users.id
            );

    UPDATE users
        SET weight_total = (
            SELECT SUM(projects.weight)
                FROM corrections
                    INNER JOIN projects
                        ON corrections.project_id = projects.id
                WHERE corrections.user_id = users.id
            );

    UPDATE users
        SET users.average_score = IF(users.weight_total = 0, 0, users.total_score_weighted / users.weight_total);
    ALTER TABLE users
        DROP COLUMN total_score_weighted;
    ALTER TABLE users
        DROP COLUMN weight_total;
END $$
DELIMITER ;
