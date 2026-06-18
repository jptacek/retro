# 🎙️ Baseball Radio CLI: Retrosheet Play-by-Play Reimagined

## 🔍 Overview

**Baseball Radio CLI** is a Python command-line application that transforms historical **Retrosheet** play-by-play data into an immersive, old-school **radio-style audio broadcast**.

Using natural language generation and voice synthesis, this app brings past baseball games to life with audio commentary that mimics traditional announcer cadence, terminology, and pacing.

---

## 🚀 Features

- 🎧 **Realistic Audio Broadcasts**  
  Converts Retrosheet event logs into spoken word using TTS (e.g., ElevenLabs, Coqui, or pyttsx3).

- 🗓️ **Historical Game Playback**  
  Replay full MLB games from 1900s to present using `.EVA` and `.EVN` files.

- 🎙️ **Dynamic Play Calling**  
  Uses templated commentary for hits, walks, strikeouts, and dramatic moments.

- 🧠 **Optional GPT-Style Commentary**  
  Plug in an LLM to enrich the narration with context, backstory, or jokes.

- 🕹️ **Simple CLI Interface**  
  ```bash
  baseball-radio --year 1975 --team BOS --game 0425
