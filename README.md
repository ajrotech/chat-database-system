# Chat System Database (Lab 10)

## Part-01 (SQL)
Files:
- `schema.sql` → creates all six tables
- `seed.sql` → inserts all provided records
- `queries.sql` → contains all required queries/operations

### Run SQL with SQLite
```bash
sqlite3 chat_system.db ".read schema.sql" ".read seed.sql"
sqlite3 chat_system.db ".read queries.sql"
```

## Part-02 (GUI + DB Integration)
A Streamlit app is provided in `app.py` and connected to `chat_system.db`.

### Features implemented
1. Template UI for Chat System Database
2. Database integration with SQLite
3. Insert / Update / Delete operations:
   - Insert message
   - Update user status
   - Update message status (Sent -> Read)
   - Delete message by `message_id`
   - Add new member to chat room
4. User statistics: messages sent per user
5. Dashboard summary:
   - Senders, receivers, total messages
   - Read/Delivered/Sent counts
   - Attachment type counts
   - Message totals by chat room

### Run the app
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deployment (Web)
### Option A: Streamlit Community Cloud (free)
1. Push this folder to a GitHub repository.
2. Go to https://share.streamlit.io/
3. Connect GitHub and select repo + `app.py`.
4. Deploy.

### Option B: Render / Railway / any paid host
- Deploy as a Python web app and set start command:
```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```
