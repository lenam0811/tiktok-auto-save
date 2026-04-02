# tiktok-auto-save
## Installation
 The project uses Python to help automatically save videos from the tiktok user-data file.
### 1. Clone the repository
 
```bash
git clone https://github.com/your-username/tiktok-auto-save.git
cd tiktok-auto-save
```
 
### 2. Install Python dependencies
 
```bash
pip install playwright
```
 
### 3. Install Chromium for Playwright
 
```bash
playwright install chromium
```
 
---
 
## Data Setup
 
### `cookies.json` — TikTok login cookies
 
You need to export cookies from your browser after logging into TikTok.
 
**How to get your cookies (using the Cookie-Editor extension):**
 
1. Log in to TikTok on Chrome or Firefox as usual.
2. Install the [Cookie-Editor](https://cookie-editor.cgagnier.ca/) extension.
3. Go to `https://www.tiktok.com`, then **save and like at least one video** so TikTok fully activates your session cookies.
4. Open the Cookie-Editor extension and click **Export** → **Export as JSON**.
5. Save the file as `cookies.json` and place it in the project folder.
 
> ⚠️ **Security note:** Cookies contain sensitive login information. Never share your `cookies.json` file with anyone.
 
---
 
### `user.json` — List of videos to save
 
This file contains your TikTok favorite videos list, exported directly from your TikTok account.
 
**How to export your personal data from TikTok:**
 
1. Go to **Settings & Privacy** on TikTok.
2. Select **Account** → **Request your data**.
3. Choose **JSON** format and submit the request.
4. TikTok will send an email with a download link — download the JSON file.
5. Rename it to `user.json` and place it in the project folder.
 
The bot will automatically locate the `FavoriteVideoList` section inside the file to extract all video links.
 
---
 
## Configuration (optional)
 
Open `config.py` to adjust the settings:
 
| Parameter | Default | Description |
|---|---|---|
| `HEADLESS_MODE` | `False` | `True` = hide browser window, `False` = show browser window |
| `MIN_DELAY` | `3.0` | Minimum wait time between videos (seconds) |
| `MAX_DELAY` | `7.0` | Maximum wait time between videos (seconds) |
 
> Avoid setting the delay too low to reduce the risk of being detected by TikTok.
 
---
 
## Running the Bot
 
Make sure your project folder looks like this before running:
 
```
tiktok-auto-save/
├── cookies.json      ← Your login cookies
├── user.json         ← Your favorite videos data
├── config.py
├── file_utils.py
├── main.py
└── tiktok_bot.py
```
 
Then run:
 
```bash
python main.py
```
 
---
 
## Notes
 
- The bot mimics real user behavior (random delays, hidden webdriver) but cannot guarantee 100% avoidance of TikTok's rate limits.
- Intended for personal use on your own account only.
- Cookies may expire after a few days — re-export them if the bot reports a login error.
