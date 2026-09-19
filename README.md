# Daily Weather Email Bot

Sends you a weather report for **singapore** by email every
morning at **6:00 AM IST**, automatically, using GitHub Actions.

## How it works

- `main.py` calls the OpenWeatherMap API for the current weather, formats
  a plain-text report, and emails it via Gmail SMTP.
- `.github/workflows/weather-email.yml` runs `main.py` on a GitHub Actions
  schedule (cron), so once it's set up you don't need your own computer on.
- You can also run `main.py` locally (e.g. from IDLE 3.10) to test it.

## One-time setup

### 1. Get an OpenWeatherMap API key
- Sign up at https://openweathermap.org/api and grab a free API key
  (the "Current Weather Data" plan is enough).
- New keys can take up to ~2 hours to activate.

### 2. Create a Gmail App Password
Gmail won't accept your normal password for SMTP from a script.
- Turn on 2-Step Verification on your Google account (Google Account →
  Security → 2-Step Verification).
- Then go to Google Account → Security → App passwords, and create one
  for "Mail". Copy the 16-character password it gives you.

### 3. Push this project to a GitHub repository
```bash
cd weather-email-bot
git init
git add .
git commit -m "Daily weather email bot"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

### 4. Add repository secrets
In your GitHub repo: **Settings → Secrets and variables → Actions → New
repository secret**, add each of:

| Secret name          | Value                                      |
|-----------------------|---------------------------------------------|
| `OWM_API_KEY`          | Your OpenWeatherMap API key                |
| `GMAIL_USER`           | Your Gmail address (the sender)            |
| `GMAIL_APP_PASSWORD`   | The 16-character App Password from step 2  |
| `TO_EMAIL`             | Where to send the report (your address)    |

### 5. Test it
Go to the **Actions** tab of your repo → **Daily Weather Email** →
**Run workflow** to trigger it manually and confirm the email arrives.
After that, it will run automatically every day at 6:00 AM IST.

## Running locally (e.g. in IDLE)

Set the same four values as environment variables before running, e.g.
in PowerShell:
```powershell
$env:OWM_API_KEY="..."
$env:GMAIL_USER="..."
$env:GMAIL_APP_PASSWORD="..."
$env:TO_EMAIL="..."
python main.py
```
Or on macOS/Linux:
```bash
export OWM_API_KEY="..."
export GMAIL_USER="..."
export GMAIL_APP_PASSWORD="..."
export TO_EMAIL="..."
python3 main.py
```

## Changing the city or time

- **City**: edit the `CITY` value in `.github/workflows/weather-email.yml`
  (format: `"City,CountryCode"`, e.g. `"Coimbatore,IN"`).
- **Time**: edit the `cron` line. GitHub Actions cron times are in UTC —
  subtract 5 hours 30 minutes from your desired IST time to get the UTC
  cron value.
