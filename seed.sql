INSERT INTO users (user_id, user_name, email, password, status, last_seen) VALUES
(1, 'Ali Khan', 'ali@gmail.com', 'ali123', 'Online', '2026-04-14 09:15 AM'),
(2, 'Sara Ahmed', 'sara@gmail.com', 'sara123', 'Offline', '2026-04-14 08:50 AM'),
(3, 'Ahmed Raza', 'ahmed@gmail.com', 'ahmed123', 'Away', '2026-04-14 09:00 AM'),
(4, 'Ayesha Noor', 'ayesha@gmail.com', 'ayesha123', 'Online', '2026-04-14 09:10 AM'),
(5, 'Bilal Hussain', 'bilal@gmail.com', 'bilal123', 'Offline', '2026-04-13 10:30 PM');

INSERT INTO chats (chat_id, send_id, receiver_id, chat_date) VALUES
(1, 1, 2, '2026-04-14'),
(2, 2, 1, '2026-04-14'),
(3, 3, 4, '2026-04-14'),
(4, 4, 5, '2026-04-13'),
(5, 1, 5, '2026-04-13');

INSERT INTO messages (message_id, chat_id, sender_id, message_text, timestamp, message_status) VALUES
(1, 1, 1, 'Hi Sara!', '2026-04-14 09:00 AM', 'Read'),
(2, 1, 2, 'Hello Ali!', '2026-04-14 09:01 AM', 'Read'),
(3, 1, 1, 'How are you?', '2026-04-14 09:02 AM', 'Delivered'),
(4, 3, 3, 'Hi Ayesha!', '2026-04-14 08:45 AM', 'Read'),
(5, 3, 4, 'Hello Ahmed!', '2026-04-14 08:46 AM', 'Sent'),
(6, 4, 4, 'Are you free?', '2026-04-13 07:30 PM', 'Delivered'),
(7, 4, 5, 'Yes, tell me.', '2026-04-13 07:32 PM', 'Read'),
(8, 5, 1, 'Hi Bilal!', '2026-04-13 09:00 PM', 'Delivered'),
(9, 5, 5, 'Hello Ali!', '2026-04-13 09:02 PM', 'Read'),
(10, 2, 2, 'See you soon.', '2026-04-14 10:00 AM', 'Sent');

INSERT INTO chatrooms (room_id, room_name) VALUES
(1, 'Computer Science'),
(2, 'Project Team'),
(3, 'Friends Group');

INSERT INTO groupmembers (room_id, user_id) VALUES
(1, 1),
(1, 2),
(1, 3),
(2, 2),
(2, 4),
(3, 1),
(3, 4),
(3, 5);

INSERT INTO attachments (attachment_id, message_id, file_name, file_type) VALUES
(1, 3, 'assignment.pdf', 'PDF'),
(2, 6, 'schedule.docx', 'DOCX'),
(3, 7, 'image.jpg', 'JPG'),
(4, 8, 'notes.txt', 'TXT'),
(5, 9, 'presentation.pptx', 'PPTX');
