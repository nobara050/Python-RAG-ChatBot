PROJECT NAME
============
Chatbot application with Retrieval-Augmented Generation (RAG) and Text-to-Speech integration.

GETTING STARTED
---------------

FRONTEND
1. Navigate to the frontend folder:
   cd frontend
2. Run the Streamlit application:
   streamlit run app.py

BACKEND
1. Place your personal data files into the data folder:
   backend/data/
2. If you add new data files, reset the database:
   python populate_database --reset
3. Run the backend API:
   uvicorn main:app --reload

API STRUCTURE
-------------

1. POST /query
   - Query data
   - Parameter: query_text (string)
   - Returns: query results based on the data

2. GET /chunks
   - Retrieve a list of data chunks
   - Returns: list of chunks

3. POST /tts
   - Convert text to speech (Text-to-Speech)
   - Parameter:
       {
           "text": "Text to be converted"
       }
   - Returns: WAV audio stream
   - Purpose: play or download audio from the provided text

USING THE API
-------------
- Send POST requests to `/query` with `query_text` to perform queries.
- Send GET requests to `/chunks` to retrieve data chunks.
- Send POST requests to `/tts` with a JSON body containing `text` to receive WAV audio.

LICENSE
-------
Information about the project license (if any)
