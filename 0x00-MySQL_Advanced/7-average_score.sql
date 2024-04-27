-- SQL script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student. Note: An average score can be a decimal

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE avg_score DECIMAL(10, 2);
    DECLARE num_subjects INT;
    DECLARE score_total DECIMAL(10, 2); -- Changed to DECIMAL
    
    -- Compute the average score for the user
    SELECT SUM(score) INTO score_total FROM corrections WHERE user_id = user_id;
    SELECT COUNT(*) INTO num_subjects FROM corrections WHERE user_id = user_id;
    
    IF num_subjects > 0 THEN
        SET avg_score = score_total / num_subjects;
    ELSE
        SET avg_score = 0;
    END IF;
    
    -- Update the user's average score in the users table
    UPDATE users SET average_score = avg_score WHERE id = user_id;
END;
//

DELIMITER ;
