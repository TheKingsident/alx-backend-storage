-- SQL script that creates a trigger that decreases the quantity of an item
-- after adding a new order.
DROP TRIGGER IF EXISTS after_insert_order;
DELIMITER //
CREATE TRIGGER after_insert_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = NEW.number
    WHERE name = items.name;
END //
DELIMITER ;
