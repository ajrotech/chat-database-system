import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).parent / "chat_system.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"
SEED_PATH = Path(__file__).parent / "seed.sql"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_database(reset: bool = False):
    conn = get_connection()
    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            schema_sql = schema_file.read()
        with open(SEED_PATH, "r", encoding="utf-8") as seed_file:
            seed_sql = seed_file.read()

        if reset:
            conn.executescript(schema_sql)
            conn.executescript(seed_sql)
        else:
            exists = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
            ).fetchone()
            if not exists:
                conn.executescript(schema_sql)
                conn.executescript(seed_sql)
        conn.commit()
    finally:
        conn.close()


def fetch_df(query: str, params=()):
    conn = get_connection()
    try:
        return pd.read_sql_query(query, conn, params=params)
    finally:
        conn.close()


def execute_query(query: str, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


st.set_page_config(page_title="Chat System Database", layout="wide")
st.title("Chat System Database")

with st.sidebar:
    st.header("Database")
    if st.button("Initialize / Reset Database"):
        init_database(reset=True)
        st.success("Database recreated with sample data.")

init_database(reset=False)

tab_view, tab_crud, tab_stats, tab_dashboard = st.tabs(
    ["Data View", "CRUD", "User Stats", "Dashboard"]
)

with tab_view:
    st.subheader("Users")
    st.dataframe(fetch_df("SELECT * FROM users ORDER BY user_id"), use_container_width=True)

    st.subheader("Chats")
    st.dataframe(fetch_df("SELECT * FROM chats ORDER BY chat_id"), use_container_width=True)

    st.subheader("Messages")
    st.dataframe(fetch_df("SELECT * FROM messages ORDER BY message_id"), use_container_width=True)

    st.subheader("Chat Rooms")
    st.dataframe(fetch_df("SELECT * FROM chatrooms ORDER BY room_id"), use_container_width=True)

    st.subheader("Group Members")
    st.dataframe(fetch_df("SELECT * FROM groupmembers ORDER BY room_id, user_id"), use_container_width=True)

    st.subheader("Attachments")
    st.dataframe(fetch_df("SELECT * FROM attachments ORDER BY attachment_id"), use_container_width=True)

with tab_crud:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Insert: Add New Message")
        chats_df = fetch_df("SELECT chat_id FROM chats ORDER BY chat_id")
        users_df = fetch_df("SELECT user_id, user_name FROM users ORDER BY user_id")

        new_chat_id = st.selectbox("Chat ID", chats_df["chat_id"].tolist(), key="ins_chat")
        sender_map = {
            f"{row.user_id} - {row.user_name}": row.user_id
            for row in users_df.itertuples(index=False)
        }
        sender_label = st.selectbox("Sender", list(sender_map.keys()), key="ins_sender")
        new_text = st.text_input("Message Text", key="ins_text")
        new_timestamp = st.text_input("Timestamp", value="2026-04-20 10:00 AM", key="ins_time")
        new_status = st.selectbox("Status", ["Sent", "Delivered", "Read"], key="ins_status")

        if st.button("Insert Message"):
            max_id_df = fetch_df("SELECT COALESCE(MAX(message_id), 0) AS max_id FROM messages")
            next_id = int(max_id_df.iloc[0]["max_id"]) + 1
            execute_query(
                """
                INSERT INTO messages (message_id, chat_id, sender_id, message_text, timestamp, message_status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (next_id, int(new_chat_id), sender_map[sender_label], new_text, new_timestamp, new_status),
            )
            st.success(f"Message inserted with message_id={next_id}")

        st.markdown("### Delete: Message")
        delete_id = st.number_input("Message ID to delete", min_value=1, step=1, value=10)
        if st.button("Delete Message"):
            deleted = execute_query("DELETE FROM messages WHERE message_id = ?", (int(delete_id),))
            if deleted:
                st.success(f"Deleted message_id={int(delete_id)}")
            else:
                st.warning("No message found with that ID.")

    with c2:
        st.markdown("### Update: User Status")
        user_options = {
            f"{row.user_id} - {row.user_name}": row.user_id
            for row in fetch_df("SELECT user_id, user_name FROM users ORDER BY user_id").itertuples(index=False)
        }
        selected_user = st.selectbox("User", list(user_options.keys()), key="upd_user")
        new_user_status = st.selectbox("New Status", ["Online", "Offline", "Away"], key="upd_user_status")
        new_seen = st.text_input("Last Seen", value="2026-04-20 10:05 AM", key="upd_seen")

        if st.button("Update User Status"):
            execute_query(
                "UPDATE users SET status = ?, last_seen = ? WHERE user_id = ?",
                (new_user_status, new_seen, user_options[selected_user]),
            )
            st.success("User status updated.")

        st.markdown("### Update: Message Status (Sent -> Read)")
        if st.button("Mark All Sent as Read"):
            changed = execute_query(
                "UPDATE messages SET message_status = 'Read' WHERE message_status = 'Sent'"
            )
            st.success(f"Updated {changed} message(s).")

        st.markdown("### Insert: Add New Member to Room")
        rooms = fetch_df("SELECT room_id, room_name FROM chatrooms ORDER BY room_id")
        room_map = {f"{row.room_id} - {row.room_name}": row.room_id for row in rooms.itertuples(index=False)}
        member_label = st.selectbox("Room", list(room_map.keys()), key="room_add")
        member_user = st.selectbox("User to Add", list(user_options.keys()), key="room_user")

        if st.button("Add Member"):
            try:
                execute_query(
                    "INSERT INTO groupmembers (room_id, user_id) VALUES (?, ?)",
                    (room_map[member_label], user_options[member_user]),
                )
                st.success("Member added to room.")
            except sqlite3.IntegrityError:
                st.warning("This user is already in that room.")

with tab_stats:
    st.subheader("How many messages each user has sent")
    stats_df = fetch_df(
        """
        SELECT u.user_id, u.user_name, COUNT(m.message_id) AS total_sent
        FROM users u
        LEFT JOIN messages m ON m.sender_id = u.user_id
        GROUP BY u.user_id, u.user_name
        ORDER BY total_sent DESC, u.user_id
        """
    )
    st.dataframe(stats_df, use_container_width=True)

    max_sender_df = fetch_df(
        """
        SELECT u.user_id, u.user_name, COUNT(m.message_id) AS total_sent
        FROM users u
        JOIN messages m ON m.sender_id = u.user_id
        GROUP BY u.user_id, u.user_name
        ORDER BY total_sent DESC, u.user_id
        LIMIT 1
        """
    )
    if not max_sender_df.empty:
        row = max_sender_df.iloc[0]
        st.info(f"Top sender: {row['user_name']} (user_id={row['user_id']}) with {row['total_sent']} messages")

    no_sender_df = fetch_df(
        """
        SELECT u.user_id, u.user_name
        FROM users u
        LEFT JOIN messages m ON m.sender_id = u.user_id
        WHERE m.message_id IS NULL
        ORDER BY u.user_id
        """
    )
    st.subheader("Users who have not sent any message")
    st.dataframe(no_sender_df, use_container_width=True)

with tab_dashboard:
    st.subheader("Summary")

    summary = {
        "Total Senders (Users)": int(fetch_df("SELECT COUNT(*) c FROM users").iloc[0]["c"]),
        "Total Receivers (distinct receiver_id)": int(
            fetch_df("SELECT COUNT(DISTINCT receiver_id) c FROM chats").iloc[0]["c"]
        ),
        "Total Messages": int(fetch_df("SELECT COUNT(*) c FROM messages").iloc[0]["c"]),
        "Read Messages": int(
            fetch_df("SELECT COUNT(*) c FROM messages WHERE message_status='Read'").iloc[0]["c"]
        ),
        "Delivered Messages": int(
            fetch_df("SELECT COUNT(*) c FROM messages WHERE message_status='Delivered'").iloc[0]["c"]
        ),
        "Sent Messages": int(
            fetch_df("SELECT COUNT(*) c FROM messages WHERE message_status='Sent'").iloc[0]["c"]
        ),
    }

    metric_cols = st.columns(3)
    for idx, (label, value) in enumerate(summary.items()):
        metric_cols[idx % 3].metric(label, value)

    st.markdown("### Attachment Type Counts")
    attachment_df = fetch_df(
        """
        SELECT file_type, COUNT(*) AS total
        FROM attachments
        GROUP BY file_type
        ORDER BY total DESC, file_type
        """
    )
    st.dataframe(attachment_df, use_container_width=True)

    st.markdown("### Total Messages by Chat Room")
    room_msg_df = fetch_df(
        """
        SELECT cr.room_id, cr.room_name, COUNT(m.message_id) AS total_messages
        FROM chatrooms cr
        LEFT JOIN groupmembers gm ON gm.room_id = cr.room_id
        LEFT JOIN messages m ON m.sender_id = gm.user_id
        GROUP BY cr.room_id, cr.room_name
        ORDER BY cr.room_id
        """
    )
    st.dataframe(room_msg_df, use_container_width=True)
