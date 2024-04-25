-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id, project_id INT;
    DECLARE user_score, total_score, total_weight FLOAT;
    DECLARE cur CURSOR FOR SELECT u.id, p.id FROM users u, projects p;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    DROP TEMPORARY TABLE IF EXISTS temp_average_scores;
    CREATE TEMPORARY TABLE temp_average_scores (
        user_id INT NOT NULL,
        average_score FLOAT
    );

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO user_id, project_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        SET total_score = 0;
        SET total_weight = 0;

        INSERT INTO temp_average_scores (user_id, average_score)
        SELECT user_id, SUM(score * weight) / SUM(weight) AS average_score
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id
        GROUP BY user_id;

    END LOOP;

    CLOSE cur;

    -- Update users table with the computed average scores
    UPDATE users u
    JOIN temp_average_scores t ON u.id = t.user_id
    SET u.average_score = t.average_score;

    DROP TEMPORARY TABLE IF EXISTS temp_average_scores;
END //

DELIMITER ;
