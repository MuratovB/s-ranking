# S-Ranking: A YouTube Playlist Ranking Application - Final Report

## 1. Introduction

S-Ranking is a web application designed to allow users to rank YouTube playlists based on their personal preferences. The application presents users with pairs of videos from a given playlist and asks them to choose which video they prefer. This process continues until the application generates a ranked list of all videos in the playlist.  The application also features a chat functionality, powered by a large language model, to allow users to discuss the playlist and videos with an AI assistant.

## 2. Features

*   **Playlist Ranking:** The core functionality of the application is to rank videos within a YouTube playlist. Users input a playlist ID or URL, and the application guides them through a pairwise comparison process.
*   **Session Management:** Users can create sessions with custom names to manage their rankings. The session name is stored in local storage to maintain continuity.
*   **YouTube API Integration:** The application utilizes the YouTube API to fetch playlist data, including video titles, thumbnails, and video IDs.
*   **User Interface:** The application provides a user-friendly interface with clear instructions, video previews, and intuitive controls.
*   **Chat Functionality:** A chat interface allows users to send messages related to the playlist and videos to a large language model, which responds with relevant information and discussion points.
*   **Rate Limiting:** Implemented using `slowapi` to prevent abuse and ensure fair usage.

## 3. Technical Design

*   **Backend:** The backend is built using FastAPI, a modern, high-performance Python web framework.
*   **Frontend:** The frontend is built using HTML, CSS, and JavaScript.
*   **Templating:** Jinja2 is used for rendering dynamic HTML content.
*   **YouTube API:** The Google's YouTube Data API v3 is used to fetch playlist information.
*   **LLM API:** Google's Generative Language API is used to power the chat functionality.
*   **State Management:** Sessions are managed in-memory using a Python dictionary.
*   **Asynchronous Tasks:** The `send_message_to_model` function is implemented as an asynchronous task to prevent blocking the main thread.
*   **Package Management:** Python dependencies are managed using `pip` and listed in `requirements.txt`.

## 4. Implementation Details

*   **`main.py`:** Contains the FastAPI application logic, including API endpoints for starting sessions, processing choices, retrieving videos, and sending messages.
*   **`utils.py`:** Includes utility functions for fetching videos from YouTube using the API and sending messages to the language model.
*   **`schemas.py`:** Defines Pydantic models for request and response data validation.
*   **`templates/index.html`:** The main HTML template for the application's user interface.
*   **`static/style.css`:** CSS file for styling the application.
*   **`static/script.js`:** JavaScript file for handling frontend logic, including user interactions and API calls.

## 5. Challenges and Solutions

*   **Rate Limiting:** The YouTube API has rate limits, which were addressed by implementing error handling and potentially could be improved by implementing caching mechanisms.
*   **Asynchronous Operations:** Integrating asynchronous tasks required careful management to ensure non-blocking behavior.
*   **UI Updates:** Dynamically updating the UI with JavaScript required managing DOM manipulation and event handling effectively.
*   **LLM Integration:** Ensuring the LLM responses were relevant and appropriate required careful prompt engineering and message filtering.

## 6. Future Enhancements

*   **Database Integration:** Persist session data in a database (e.g., PostgreSQL) for scalability and persistence.
*   **User Authentication:** Implement user authentication to allow users to save and manage their ranked playlists.
*   **Advanced Ranking Algorithms:** Explore more sophisticated ranking algorithms, such as Elo rating or TrueSkill.
*   **Improved UI/UX:** Enhance the user interface with features like drag-and-drop sorting and visual progress indicators.
*   **Real-time Updates:** Implement real-time updates using WebSockets to provide a more interactive experience.
*   **More Robust Error Handling:** Implement more robust error handling and logging to improve the application's reliability.
*   **Expand LLM Functionality:** Add more features to the LLM integration, such as sentiment analysis or topic extraction.

## 7. Conclusion

S-Ranking provides a functional and engaging platform for ranking YouTube playlists. The application effectively leverages the YouTube API and FastAPI framework to deliver a user-friendly experience. While there are opportunities for future enhancements, the current implementation provides a solid foundation for further development and expansion.
