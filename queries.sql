-- Part-01 Required SQL Operations

-- 1) Create above six tables and insert all entries
-- Run:
-- .read schema.sql
-- .read seed.sql

-- 2) Add a new member to a chat room
INSERT INTO groupmembers (room_id, user_id) VALUES (2, 5);

-- 3) Update a user's status to Online
UPDATE users
SET status = 'Online', last_seen = '2026-04-20 10:00 AM'
WHERE user_id = 2;

-- 4) Update the message status from Sent to Read
UPDATE messages
SET message_status = 'Read'
WHERE message_status = 'Sent';

-- 5) Delete a message with a specific message_id
DELETE FROM messages
WHERE message_id = 10;

-- 6) Retrieve all messages sent by user_id 1
SELECT message_id, chat_id, sender_id, message_text, timestamp, message_status
FROM messages
WHERE sender_id = 1
ORDER BY message_id;

-- 7) Display all users who are currently online
SELECT user_id, user_name, email, status, last_seen
FROM users
WHERE status = 'Online'
ORDER BY user_id;

-- 8) Count the total number of messages in each chat room
-- Assumption: room message count is based on messages sent by users who are members of each room
SELECT cr.room_id, cr.room_name, COUNT(m.message_id) AS total_messages
FROM chatrooms cr
LEFT JOIN groupmembers gm ON gm.room_id = cr.room_id
LEFT JOIN messages m ON m.sender_id = gm.user_id
GROUP BY cr.room_id, cr.room_name
ORDER BY cr.room_id;

-- 9) Retrieve sender who has sent maximum messages
SELECT u.user_id, u.user_name, COUNT(m.message_id) AS total_sent
FROM users u
JOIN messages m ON m.sender_id = u.user_id
GROUP BY u.user_id, u.user_name
ORDER BY total_sent DESC, u.user_id
LIMIT 1;

-- 10) Retrieve sender who has not sent any single message
SELECT u.user_id, u.user_name
FROM users u
LEFT JOIN messages m ON m.sender_id = u.user_id
WHERE m.message_id IS NULL
ORDER BY u.user_id;
