PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS attachments;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS chats;
DROP TABLE IF EXISTS groupmembers;
DROP TABLE IF EXISTS chatrooms;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Online', 'Offline', 'Away')),
    last_seen TEXT NOT NULL
);

CREATE TABLE chats (
    chat_id INTEGER PRIMARY KEY,
    send_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    chat_date TEXT NOT NULL,
    FOREIGN KEY (send_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES users(user_id)
);

CREATE TABLE messages (
    message_id INTEGER PRIMARY KEY,
    chat_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    message_text TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    message_status TEXT NOT NULL CHECK (message_status IN ('Sent', 'Delivered', 'Read')),
    FOREIGN KEY (chat_id) REFERENCES chats(chat_id),
    FOREIGN KEY (sender_id) REFERENCES users(user_id)
);

CREATE TABLE chatrooms (
    room_id INTEGER PRIMARY KEY,
    room_name TEXT NOT NULL UNIQUE
);

CREATE TABLE groupmembers (
    room_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (room_id, user_id),
    FOREIGN KEY (room_id) REFERENCES chatrooms(room_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE attachments (
    attachment_id INTEGER PRIMARY KEY,
    message_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    file_type TEXT NOT NULL,
    FOREIGN KEY (message_id) REFERENCES messages(message_id)
);
