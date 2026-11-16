# Language Audio Lessons

A flashcard-style web app for building your own audio language lessons. Swipe through cards (like or skip), and the app turns the cards you liked into a single audio lesson you can play or download.

**Status:** work in progress.

## Features

- Pick a language and browse phrase cards (English, target language, level, grammar point)
- Like or skip each card; decisions are saved to the database
- Generate an audio lesson from your liked cards (English prompt, pause, target phrase repeated twice)
- Play the lesson in the browser or download it
- Add your own cards with a form
- Japanese cards can store kanji and hiragana together as `kanji|hiragana` (the audio uses the hiragana half)

## Tech Stack

- **Frontend:** React, TypeScript, Vite, React Router
- **Backend:** Flask, Flask-CORS
- **Database:** PostgreSQL (psycopg2)
- **Audio:** edge-tts (text to speech), pydub, ffmpeg, pandas

## Prerequisites

- Node.js and npm
- Python 3.10+
- PostgreSQL
- [ffmpeg](https://ffmpeg.org/download.html), installed and on your PATH

## Setup

### 1. Database

Create these tables in PostgreSQL (adjust types as needed):

```sql
CREATE TABLE cards (
  id SERIAL PRIMARY KEY,
  english_text VARCHAR(100) NOT NULL,
  target_text VARCHAR(100) NOT NULL,
  language VARCHAR(50) NOT NULL,
  level VARCHAR(50) NOT NULL,
  grammar_point VARCHAR(100) NOT NULL
);

CREATE TABLE user_cards (
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  card_id INTEGER NOT NULL REFERENCES cards(id) ON DELETE CASCADE,
  decision VARCHAR(50) NOT NULL,
  PRIMARY KEY (user_id, card_id)
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  target_language VARCHAR(100) NOT NULL,
  user_level VARCHAR(50) NOT NULL
);

```

The connection settings are in `DataBase.py` (default host `localhost`, port `5433`).

```
Run the server:

```bash
python app.py
```

The API runs at `http://localhost:5000`.

Frontend

```bash
npm install
npm run dev
```

The app runs at `http://localhost:5173`.

## How to Use

1. Open the app and choose a language on the home page.
2. Swipe through cards with **like** or **skip**.
3. Use **Make Lesson** to generate audio from the cards you liked.
4. Play or download the lesson.
5. Use **Make Your Own Card** to add new cards.

## Project Structure

```
app.py            Flask routes
DataBase.py       PostgreSQL queries
audioexport.py    Text-to-speech and lesson audio builder
src/              React components (Home, CardDisplay, MakeCard, App, Player, Main)
```

## API Endpoints

| Method | Route | Purpose |
|---|---|---|
| GET | `/<language>` | Get all cards for a language |
| POST | `/api/cards/submit` | Add a new card |
| POST | `/api/cards/<id>/decision` | Save a like or skip |
| POST | `/api/cards/makeLesson` | Generate the audio lesson |

## Known Issues and Limitations

- User accounts are not set up yet; all decisions are saved under a temporary hard-coded user ID
- Lessons are exported as WAV, so files are larger than MP3. MP3 currently isn't working
- Card text is not validated, so incorrect spelling leads to incorrect pronunciation

## Roadmap

- User accounts and sessions
- Add spaced repition learning
- Customize audio player
- Unit test functions to check all possible edge cases
- More styling and mobile layout
- More languages

- Text-to-speech uses Microsoft Edge voices through `edge-tts`, so generating lessons requires an internet connection.