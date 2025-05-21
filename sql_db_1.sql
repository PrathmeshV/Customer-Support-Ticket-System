use ticket_sql_db;
show tables;
select *
from user1;
drop table user1;
CREATE TABLE user1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
ALTER TABLE user1
ADD UNIQUE (email);
DELIMITER // CREATE PROCEDURE CheckUserExists(
    IN input_name VARCHAR(100),
    IN input_email VARCHAR(100)
) BEGIN
SELECT *
FROM user1
WHERE name = input_name
    AND email = input_email;
END // DELIMITER;
-- delimiter //
-- CREATE TRIGGER set_priority_before_insert
-- BEFORE INSERT ON ticket_table
-- FOR EACH ROW
-- BEGIN
--   IF NEW.category = 'Softwar'  THEN
--     SET NEW.priority = 'Critical';
--   ELSEIF NEW.category = 'Hardware' THEN
--     SET NEW.priority = 'High';
--   ELSEIF NEW.category = 'Network' THEN
--     SET NEW.priority = 'Medium';
--   ELSE
--     SET NEW.priority = 'Low';
--   END IF;
-- END; //
-- delimiter ;
DELIMITER // CREATE TRIGGER before_ticket_insert BEFORE
INSERT ON ticket FOR EACH ROW BEGIN IF NEW.priority IS NULL
    OR NEW.priority = '' THEN IF NEW.category = 'Software' THEN
SET NEW.priority = 'High';
ELSEIF NEW.category = 'Network' THEN
SET NEW.priority = 'Medium';
ELSEIF NEW.category = 'Hardware' THEN
SET NEW.priority = 'Low';
ELSE
SET NEW.priority = 'Very Low';
END IF;
END IF;
END;
// DELIMITER;
CREATE TABLE ticket (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    priority VARCHAR(50) default 'Low',
    category VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'Open',
    FOREIGN KEY (user_id) REFERENCES user1(id)
);
select *
from ticket;
CREATE TABLE admin_action_log (
    action_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_id INT NOT NULL,
    -- Admin Employee ID
    ticket_id INT NOT NULL,
    -- Ticket ID being handled
    category VARCHAR(100) NOT NULL,
    -- Category of the ticket
    action VARCHAR(255) NOT NULL,
    -- Status change like "In Progress", "Resolved"
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id)
);
CREATE TABLE admin (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    -- Admin's assigned category
    priority_handling VARCHAR(50) NOT NULL -- Admin's priority handling (Low/Medium/High)
);
CREATE TABLE Feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    rating INT NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
delete from ticket
where ticket_id > 6;
drop table feedback;
select *
from ticket;
select *
from user1;
select *
from feedback;
select *
from user2;
select *
from admin_action_log;