# S-Ranking

## Overview

S-Ranking is a web application that allows users to rank YouTube playlists by comparing videos in a pairwise manner. It uses a FastAPI backend, a JavaScript frontend, and the YouTube API.

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd s-ranking
    ```

2.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**

    *   Create a `.env` file in the project root.
    *   Add your YouTube API key and NLP Model API key to the `.env` file:

        ```
        YOUTUBE_API=YOUR_YOUTUBE_API_KEY
        NLP_MODEL_API=YOUR_NLP_MODEL_API_KEY
        ```

    *   Make sure to replace `YOUR_YOUTUBE_API_KEY` and `YOUR_NLP_MODEL_API_KEY` with your actual API keys.

## Running the Application

1.  **Start the FastAPI backend:**

    ```bash
    uvicorn main:app --reload
    ```

    This command starts the FastAPI server with hot reloading enabled.  The server will be accessible at `http://127.0.0.1:8000`.

2.  **Access the application:**

    Open your web browser and navigate to `http://127.0.0.1:8000`.

## Project Structure

```
s-ranking/
├── .env              # Environment variables (API keys)
├── .gitignore        # Specifies intentionally untracked files that Git should ignore
├── main.py           # FastAPI application
├── README.md         # Documentation
├── requirements.txt  # Python dependencies
├── schemas.py        # Pydantic models for data validation
├── static/           # Static files (CSS, JavaScript)
│   ├── script.js     # Frontend logic
│   └── style.css     # Styling
├── templates/        # Jinja2 templates
│   └── index.html    # Main HTML template
└── utils.py          # Utility functions (YouTube API calls, LLM interaction)
```

## API Endpoints

*   `GET /`: Serves the main HTML page.
*   `POST /start_session`: Starts a new ranking session.  Requires `playlist_id` and `session_name` in the request body.
*   `GET /get_videos`: Retrieves the next pair of videos to be ranked.  Requires `session_name` as a query parameter.
*   `POST /process_choice`: Processes the user's choice for a pair of videos.  Requires `session_name` and `winner` (0 or 1) in the request body.
*   `POST /send_message`: Sends a message to the chat model. Requires `session_name` and `message` in the request body.

## Dependencies

*   FastAPI: Web framework
*   uvicorn: ASGI server
*   requests: HTTP requests
*   python-dotenv: Loads environment variables from a .env file
*   Jinja2: Templating engine
*   slowapi: Rate limiting

## Notes

*   The application uses in-memory storage for session data.  This means that sessions will be lost when the server restarts.  For production deployments, consider using a database.
*   The YouTube API has rate limits.  Be mindful of these limits when using the application.
*   The chat functionality is powered by a large language model.  The quality of the responses may vary.
