import requests
from twilio.rest import Client

def get_weather(api_key, location="Johns Creek,US"):
    """Get current weather data for Johns Creek, GA"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'imperial'  # For Fahrenheit
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

def send_sms(message, to_number, twilio_account_sid, twilio_auth_token, twilio_phone_number):
    """Send SMS using Twilio"""
    client = Client(twilio_account_sid, twilio_auth_token)
    
    try:
        message = client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=to_number
        )
        print(f"SMS sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

def main():
    # Configuration - replace these with your actual credentials
    OPENWEATHER_API_KEY = 'your_openweather_api_key'
    TWILIO_ACCOUNT_SID = 'your_twilio_account_sid'
    TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'
    TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'  # Must be a Twilio number in E.164 format
    RECIPIENT_NUMBER = '+16785759889'  # Number to send to in E.164 format
    
    # Get weather data
    weather = get_weather(OPENWEATHER_API_KEY, "Johns Creek,US")
    
    if weather:
        # Format the weather message
        weather_message = (
            f"Weather in Johns Creek, GA:\n"
            f"Current Temp: {weather['temp']}°F (Feels like {weather['feels_like']}°F)\n"
            f"Conditions: {weather['description'].capitalize()}\n"
            f"Humidity: {weather['humidity']}%\n"
            f"Wind: {weather['wind_speed']} mph"
        )
        
        # Send the SMS
        send_sms(weather_message, RECIPIENT_NUMBER, 
                TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER)
    else:
        print("Failed to get weather data. SMS not sent.")

if __name__ == "__main__":
    main()