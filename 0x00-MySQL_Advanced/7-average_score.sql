-- SQL script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student. Note: An average score can be a decimal
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
  IN user_id INT
)
BEGIN
  DECLARE total_score DECIMAL(10,2);  -- To store total score with decimals
  DECLARE num_corrections INT;

  -- Initialize variables
  SET total_score = 0;
  SET num_corrections = 0;

  -- Calculate total score and number of corrections for the user
  SELECT SUM(score), COUNT(*)
  INTO total_score, num_corrections
  FROM corrections
  WHERE user_id = user_id;

  -- Update user's average score (handle division by zero)
  IF num_corrections > 0 THEN
    UPDATE users
    SET average_score = total_score / num_corrections
    WHERE id = user_id;
  ELSE
    -- Set average score to 0 if no corrections found
    UPDATE users
    SET average_score = 0
    WHERE id = user_id;
  END IF;
END //

DELIMITER ;

