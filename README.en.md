🌐 Available languages: 🇺🇸 [English](README.en.md) | 🇪🇸 [Español](README.md)

# 🎧 Empy Discord Music Bot (Python)

A simple and cute music bot that runs in local for Discord using `discord.py` and `yt-dlp` libraries. Supports queues, playlists (WIP), pause/resume, and more!  
Each bot message comes with a unique kaomoji to keep things fun~ (＾▽＾)

---

# 📦 Features

- ✅ Join and leave voice channels
- 🎵 Play songs and YouTube playlists (WIP)
- ⏯️ Pause / resume
- ⏩ Skip current song
- 🗑️ Clear or remove from queue
- 📜 Show current queue
- 💌 Cute kaomojis with every response!

---

# 🔧 Requirements

- Python 3.9 or higher
- [FFmpeg](https://ffmpeg.org/download.html)
- A Discord Bot Token

---

# 🚀 Installation

1. **Clone this repository**
```bash
git clone https://github.com/your-username/your-private-repo.git
cd your-private-repo
```

2. **Create and activate a virtual environment (optional)**
```bash
python -m venv venv
venv\Scripts\activate    # On Windows
# or
source venv/bin/activate # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create a .env file in the root folder and add your bot token and guild ID (Application ID):**
```ini
DISCORD_TOKEN='YOUR_BOT_TOKEN_HERE'
GUILD_ID='YOUR_GUILD_ID'
```

# 🎥 FFmpeg Setup

This project uses FFmpeg for audio playback.

## Option 1: Use Portable FFmpeg (Recommended for Local Use)

1. Download the latest Windows build from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
2. Extract the folder (e.g., ffmpeg-master-latest-win64-gpl-shared/) into the project root.
3. The bot is already configured to use the ffmpeg.exe inside that folder.

```vbnet
ffmpeg-master-latest-win64-gpl-shared/
```

## Option 2: Add FFmpeg to your system's PATH

You can add the bin/ folder inside FFmpeg to your PATH environment variable so ffmpeg can be accessed globally.

# 🐣 Running the bot
```bash
python bot.py
```

# ✨ Example Commands
```diff
/join
/play <url>
/pause
/resume
/skip
/queue
/remove <index>
/clearqueue
/leave
```

# 💖 Credits
Made with love using:

- discord.py

- yt-dlp

- FFmpeg

# 📬 Colaborations

This project is public for everyone to enjoy and learn~ 🎶

I don't accept direct contributions without prior discussion.

If you'd like to suggest any changes or work together, please don't hesitate to contact me (｡•̀ᴗ-)✧

## Let the music begin~ ♪ヽ(･ˇ∀ˇ･ゞ)