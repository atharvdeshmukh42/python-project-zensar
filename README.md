# Social Network API with Python and Oracle DB

A RESTful API implementation for a social networking system using Python Flask and Oracle Database. This project provides endpoints for core social networking features like posting content, managing friend requests, and displaying newsfeeds.

## Features

- **User Newsfeed**: Fetch personalized newsfeed for users
- **Post Management**: Create and manage user posts
- **Friend System**: Send and accept friend requests
- **Oracle Database Integration**: Robust database backend using Oracle stored procedures

## Prerequisites

- Python 3.x
- Oracle Database
- `oracledb` Python package
- Flask

## Environment Variables

The application uses the following environment variables:

```
DB_DSN - Oracle database DSN (default: localhost:1521/XE)
DB_USER - Database username (default: system)
DB_PASSWORD - Database password
```

## API Endpoints

### Get User Newsfeed
```
GET /api/newsfeed/<user_id>
```
Returns a personalized newsfeed for the specified user.

**Response Format:**
```json
{
    "newsfeed": [
        "Post ID: 2",
        "Username: B",
        "Content: Excited to share my first post!",
        "Created At: 2025-01-12 10:30:00"
    ]
}
```

### Create New Post
```
POST /api/posts
```
Create a new post in the social network.

**Request Body:**
```json
{
    "user_id": 1,
    "content": "This is my first post using the API!"
}
```

### Send Friend Request
```
POST /api/friend-request
```
Send a friend request from one user to another.

**Request Body:**
```json
{
    "user_id1": 1,
    "user_id2": 3
}
```

### Accept Friend Request
```
POST /api/accept-friend-request
```
Accept a pending friend request.

**Request Body:**
```json
{
    "user_id1": 1,
    "user_id2": 3
}
```

## Database Integration

The application uses Oracle stored procedures for data operations:
- `display_newsfeed`: Retrieves user's newsfeed
- `add_post`: Creates a new post
- `send_friend_request`: Initiates a friend request
- `accept_friend_request`: Accepts a pending friend request

## Error Handling

The API implements comprehensive error handling for:
- Database connection failures
- Invalid request parameters
- Database operation errors

## Running the Application

1. Set up your Oracle database and create necessary stored procedures
2. Configure environment variables
3. Install dependencies:
   ```bash
   pip install flask oracledb
   ```
4. Run the application:
   ```bash
   python python-sql-connection.py
   ```
   The server will start on `http://localhost:5000`

## Security Considerations

- Database credentials are managed through environment variables
- Input validation is implemented for all endpoints
- Database connections are properly closed after each operation

## Future Improvements

- Add user authentication and authorization
- Implement post deletion and updating
- Add comment and like functionality
- Include pagination for newsfeed
- Add user profile management

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.
