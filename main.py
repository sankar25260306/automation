import smtplib
import sys
import requests

from datetime import datetime
from email.mime.text import MIMEText

load_dotenv()

# ==============================
# CONFIGURATION
# ==============================

OWM_API_KEY = "3b66888ac7448eedc14a7355d2b1e785"
GMAIL_USER = "1212sankar1212@gmail.com"
GMAIL_APP_PASSWORD = "tdmnxupmkhmnwtgc"

TO_EMAIL = "25sankar25@gmail.com"
CITY = "Singapore,SG"

# ==============================
# DISPLAY
# ==============================

print("City:", CITY)
print("Email:", GMAIL_USER)

OWM_URL = "https://api.openweathermap.org/data/2.5/weather"


# ==============================
# FETCH WEATHER
# ==============================

def fetch_weather(city: str, api_key: str) -> dict:
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(
        OWM_URL,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


# ==============================
# FORMAT WEATHER REPORT
# ==============================

def format_report(data: dict) -> tuple[str, str]:

    city_name = data.get("name", CITY)

    weather = data["weather"][0]["description"].title()

    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    temp_min = data["main"]["temp_min"]
    temp_max = data["main"]["temp_max"]

    humidity = data["main"]["humidity"]

    wind_speed = data["wind"]["speed"]

    sunrise = datetime.fromtimestamp(
        data["sys"]["sunrise"]
    ).strftime("%I:%M %p")

    sunset = datetime.fromtimestamp(
        data["sys"]["sunset"]
    ).strftime("%I:%M %p")

    today = datetime.now().strftime(
        "%A, %d %B %Y"
    )

    subject = f"Weather Report for {city_name} - {today}"

    body = f"""
Good morning!

Here is your weather report for {city_name} ({today}):

Condition:    {weather}
Temperature:  {temp}°C (feels like {feels_like}°C)
Range:        {temp_min}°C - {temp_max}°C
Humidity:     {humidity}%
Wind Speed:   {wind_speed} m/s
Sunrise:      {sunrise}
Sunset:       {sunset}

Have a great day!
"""

    return subject, body


# ==============================
# SEND EMAIL
# ==============================

def send_email(
    subject: str,
    body: str,
    to_email: str,
    gmail_user: str,
    gmail_app_password: str
) -> None:

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = to_email

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            gmail_user,
            gmail_app_password
        )

        server.sendmail(
            gmail_user,
            [to_email],
            msg.as_string()
        )


# ==============================
# MAIN
# ==============================

def main() -> None:

    if not OWM_API_KEY:
        print("OpenWeather API key is missing.")
        sys.exit(1)

    if not GMAIL_USER:
        print("Gmail user is missing.")
        sys.exit(1)

    if not GMAIL_APP_PASSWORD:
        print("Gmail app password is missing.")
        sys.exit(1)

    try:

        print("Fetching weather...")

        data = fetch_weather(
            CITY,
            OWM_API_KEY
        )

        print("Weather data received.")

        subject, body = format_report(data)

        print("Sending email...")

        send_email(
            subject,
            body,
            TO_EMAIL,
            GMAIL_USER,
            GMAIL_APP_PASSWORD
        )

        print(
            f"Weather email sent successfully to {TO_EMAIL}."
        )

    except requests.RequestException as e:

        print(
            f"Failed to fetch weather data: {e}",
            file=sys.stderr
        )

        sys.exit(1)

    except smtplib.SMTPException as e:

        print(
            f"Failed to send email: {e}",
            file=sys.stderr
        )

        sys.exit(1)


# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    main()
