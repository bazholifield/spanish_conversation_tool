# Spanish Conversation Practice Tool

While living in Spain, I built this conversation practice tool so I wouldn't feel as nervous speaking Spanish in real life.

It asks you questions in Spanish, listens to your answers, and asks follow-up questions without AI, just basic pattern matching like old chatbots. At the end it saves a transcript where you can click on any word to see what it means and how to conjugate it.

## What you need

```
pip install -r requirements.txt
python -m spacy download es_core_news_sm
```

## How to run it

```
python main.py
```

By default it runs in text mode (just type your answers). To use your microphone, open `config/settings.py` and change `INPUT_MODE = "text"` to `INPUT_MODE = "speech"`.

Say or type `salir` to end the session. Your transcript gets saved to the `transcripts/` folder — open it in a browser to look up words.

## Notes

- The follow-up questions are rule-based so it can feel a bit robotic sometimes
- The speech recognition uses Google so you need an internet connection
- I mostly use this to practice before going to the market or whatever
