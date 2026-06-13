# Reddit Listener API

A FastAPI backend for Reddit content monitoring and alerting. This API allows users to configure their preferences for subreddits and keywords, then receive filtered Reddit posts that match their criteria.

## Features

- **User Configuration**: Users can set their preferred subreddits and keywords
- **Smart Filtering**: Posts are filtered based on user's subreddit and keyword preferences
- **Real-time Data**: Tracks the last sync time from Reddit
- **Authentication**: JWT-based authentication with Better Auth integration
- **Supabase Integration**: Uses Supabase as the database backend

## Tech Stack

- **Framework**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **Authentication**: JWT + Better Auth
- **Python**: 3.13+

## Setup

### Prerequisites

1. Python 3.13 or higher
2. Supabase project
3. Better Auth setup (optional)

### Environment Variables

Create a `.env` file in the root directory:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# Authentication
JWT_SECRET=your-jwt-secret-key
JWT_ALGORITHM=HS256

# Better Auth (optional)
BETTER_AUTH_URL=http://localhost:3000/api/auth

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### Installation

1. Install dependencies:
```bash
uv sync
```

2. Set up the database tables in Supabase:

```sql
-- User configurations table
CREATE TABLE IF NOT EXISTS user_configs (
    id uuid primary key,
    subreddits text[] not null,
    keywords text[] not null
);

-- Matches table for Reddit posts
CREATE TABLE IF NOT EXISTS matches (
    id text primary key,
    reddit_id text not null,
    type text not null,
    subreddit text not null,
    title text not null,
    content text,
    url text,
    upvotes integer,
    num_comments integer,
    ratio float,
    intent_score float,
    matched_keywords text[],
    sentiment text,
    user_ids uuid[],
    timestamp timestamptz not null
);

-- Metadata table for sync tracking
CREATE TABLE IF NOT EXISTS metadata (
    id integer primary key,
    job_name text not null,
    synced timestamptz not null
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_matches_timestamp ON matches(timestamp);
CREATE INDEX IF NOT EXISTS idx_matches_reddit_id ON matches(reddit_id);
```

3. Run the application:
```bash
uv run python -m app.main
```

The API will be available at `http://localhost:8000`

## API Documentation

### Authentication

All endpoints require authentication via Bearer token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Endpoints

#### User Configuration

**GET** `/api/user/config`
- Get the current user's configuration
- Returns: `UserConfig` object with subreddits and keywords

**PUT** `/api/user/config`
- Update the user's configuration
- Body: `UserConfigUpdate` object
- Returns: Updated `UserConfig` object

#### Matches

**GET** `/api/matches`
- Get filtered Reddit posts that match user's criteria
- Query parameters:
  - `limit` (optional): Number of posts to return (1-100, default: 50)
  - `offset` (optional): Number of posts to skip (default: 0)
- Returns: Array of `Match` objects

**GET** `/api/matches/{match_id}`
- Get a specific match by ID
- Returns: `Match` object

#### Metadata

**GET** `/api/metadata/sync-time`
- Get the last sync time from Reddit
- Returns: Object with `job_name` and `synced` timestamp

**GET** `/api/metadata`
- Get all metadata entries
- Returns: Array of `Metadata` objects

#### Health Check

**GET** `/api/health`
- Health check endpoint
- Returns: Health status and timestamp

### Data Models

#### UserConfig
```json
{
  "id": "uuid",
  "subreddits": ["subreddit1", "subreddit2"],
  "keywords": ["keyword1", "keyword2"]
}
```

#### Match
```json
{
  "id": "string",
  "reddit_id": "string",
  "type": "string",
  "subreddit": "string",
  "title": "string",
  "content": "string",
  "url": "string",
  "upvotes": 123,
  "num_comments": 45,
  "ratio": 0.95,
  "intent_score": 0.8,
  "matched_keywords": ["keyword1", "keyword2"],
  "sentiment": "positive",
  "user_ids": ["uuid1", "uuid2"],
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### Metadata
```json
{
  "id": 1,
  "job_name": "reddit_sync",
  "synced": "2024-01-01T12:00:00Z"
}
```

## Filtering Logic

The API implements smart filtering based on user preferences:

1. **Subreddit Filtering**: Posts must be from one of the user's configured subreddits
2. **Keyword Filtering**: Posts must contain at least one of the user's keywords in the `matched_keywords` array
3. **User Association**: Posts are associated with users via the `user_ids` array
4. **Combined Logic**: Both subreddit AND keyword criteria must be met (AND logic)

## Frontend Integration

### Example Usage

```javascript
// Get user configuration
const config = await fetch('/api/user/config', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

// Update user configuration
const updatedConfig = await fetch('/api/user/config', {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    subreddits: ['programming', 'python'],
    keywords: ['fastapi', 'supabase']
  })
});

// Get filtered matches
const matches = await fetch('/api/matches?limit=20&offset=0', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

// Get last sync time
const syncInfo = await fetch('/api/metadata/sync-time', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

### Error Handling

The API returns standard HTTP status codes:

- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `500`: Internal Server Error

Error responses include a `detail` field with error information.

## Development

### Running in Development

```bash
# Install dependencies
uv sync

# Run with auto-reload
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Testing

```bash
# Run tests (when implemented)
uv run pytest
```

## Deployment

### Environment Setup

1. Set up a Supabase project
2. Configure environment variables
3. Create database tables using the SQL provided above
4. Deploy to your preferred platform (Vercel, Railway, etc.)

### Production Considerations

- Use environment variables for all sensitive configuration
- Set up proper CORS configuration for your frontend domain
- Configure Supabase Row Level Security (RLS) policies
- Set up monitoring and logging
- Use HTTPS in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License
](https://bulkctc.com)
