# Note APIs 

## Authentication
All endpoints require authentication using Token-based authentication. You need to include the token in the headers of your HTTP requests.

**Example:**

```http
Authorization: Token generated_token_here
```
### [User Authentication APIs 🔗 ](https://github.com/mandharet/notes-crud/tree/DEVELOPMENT/apps/authapp#user-authentication-apis)

------------

## 1. Get List of Notes

**Endpoint:** `GET /notes`

**Description:** Retrieve a list of notes with their details.

**Response (200 OK):**
```json
[
  {
    "content": [
      {"line_no": 1, "text": "Note content line 1"},
      {"line_no": 2, "text": "Note content line 2"}
    ],
    "modified-by": "user1",
    "modified-on": "2024-02-18T12:34:56",
    "noteId": 1,
    "owner": "owner1",
    "sharedWith": "user2,user3",
    "versionHash": 123
  },
  // ... (more notes)
]
```

**Response (404 Not Found):**
```json
{
  "error": "No notes found for the user"
}
```

## 2. Create a Note

**Endpoint:** `POST /notes/create`

**Description:** Create a new note.

**Request:**
```json
{
  "noteContent": "Note content line 1\nNote content line 2"
}
```

**Response (201 Created):**
```json
{
  "message": "Note created successfully"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Note Content is required"
}
```

## 3. Get a Note

**Endpoint:** `GET /notes/{note_id}`

**Description:** Retrieve a specific note by its ID.

**Request:**
- Method: `GET`

**Response (200 OK):**
```json
{
  "content": [
    {"line_no": 1, "text": "Note content line 1"},
    {"line_no": 2, "text": "Note content line 2"}
  ],
  "modified-by": "user1",
  "modified-on": "2024-02-18T12:34:56",
  "noteId": 1,
  "owner": "owner1",
  "sharedWith": "user2,user3",
  "versionHash": 123
}
```

**Response (404 Not Found):**
```json
{
  "error": "Note not found"
}
```

## 4. Update a Note

**Endpoint:** `PUT /notes/{note_id}`

**Description:** Update the content of a specific note by its ID.

**Request:**
```json
{
  "noteContent": "Updated note content line 1\nUpdated note content line 2"
}
```

**Response (200 OK):**
```json
{
  "message": "Note updated successfully"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Note Content is required"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Note not found"
}
```

## 5. Share a Note

**Endpoint:** `POST /notes/share`

**Description:** Share a note with other users.

**Request:**
```json
{
  "noteId": 1,
  "sharedUsers": [2, 3]
}
```

**Response (200 OK):**
```json
{
  "message": "Note shared successfully"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Note Id is required"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Note not found"
}
```

## 6. Get Version History

**Endpoint:** `GET /notes/version-history/{note_id}`

**Description:** Retrieve the version history of a specific note.

**Response (200 OK):**
```json
[
  {
    "versionHash": 123,
    "modified-on": "2024-02-18T12:34:56",
    "modified-by": "user1",
    "changes": [
      {"line_no": 1, "text": "Note content line 1"},
      {"line_no": 2, "text": "Note content line 2"}
    ]
  },
  // ... (more versions)
]
```

**Response (404 Not Found):**
```json
{
  "error": "Note not found"
}
```
