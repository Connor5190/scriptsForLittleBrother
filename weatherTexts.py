import requests
from dotenv import load_dotenv
import os

def get_weather(api_key, location="Johns Creek,US"):
    """Get current weather data for Johns Creek, GA"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'imperial'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather_info = {
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed']
        }
        return weather_info
    except Exception as e:
        print(f"Error getting weather data: {e}")
        return None

def send_sms(message, to_number, textbelt_api_key):
    """Send SMS using Textbelt"""
    url = "https://textbelt.com/text"
    payload = {
        'phone': to_number,
        'message': message,
        'key': textbelt_api_key
    }
        
    try:
        response = requests.post(url, data=payload)
        result = response.json()
        print(f"Response from Textbelt: {result}")
        if result.get('success'):
            print("SMS sent successfully!")
        else:
            print(f"Failed to send SMS: {result.get('error')}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

def main():
    load_dotenv()  # Load environment variables from .env file

    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    TEXTBELT_API_KEY = os.getenv("TEXTBELT_API_KEY")  # e.g., 'textbelt' for free usage
    RECIPIENT_NUMBER = os.getenv("RECIPIENT_NUMBER")  # E.164 or local format

    weather = get_weather(OPENWEATHER_API_KEY, "Johns Creek,US")
    
    if weather:
        weather_message = (
            f"Expect a high of {weather['temp']}°F, feeling like {weather['feels_like']}°, "
            f"with {weather['description']} skies. Humidity at {weather['humidity']}%, "
            f"and winds around {weather['wind_speed']} mph. Stay cool out there. "
            "Today’s verse: Proverbs 3:5 — “Trust in the Lord with all your heart and lean not on your own understanding.”"
        )

        print(weather_message)
        send_sms(weather_message, RECIPIENT_NUMBER, TEXTBELT_API_KEY)
    else:
        print("Failed to get weather data. SMS not sent.")

if __name__ == "__main__":
    main()
