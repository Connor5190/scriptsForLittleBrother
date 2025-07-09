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
    bible_verses = [
    "Psalm 55:22 - Cast your cares on the Lord and he will sustain you; he will never let the righteous be shaken.",
    "Isaiah 41:10 - So do not fear, for I am with you; do not be dismayed, for I am your God. I will strengthen you and help you; I will uphold you with my righteous right hand.",
    "Philippians 4:6-7 - Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.",
    "Matthew 11:28 - Come to me, all you who are weary and burdened, and I will give you rest.",
    "Proverbs 3:5-6 - Trust in the Lord with all your heart and lean not on your own understanding; in all your ways submit to him, and he will make your paths straight.",
    "Romans 8:28 - And we know that in all things God works for the good of those who love him, who have been called according to his purpose.",
    "Joshua 1:9 - Have I not commanded you? Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go.",
    "2 Corinthians 12:9 - But he said to me, 'My grace is sufficient for you, for my power is made perfect in weakness.'",
    "Psalm 23:1 - The Lord is my shepherd, I lack nothing.",
    "John 14:27 - Peace I leave with you; my peace I give you. I do not give to you as the world gives. Do not let your hearts be troubled and do not be afraid.",
    "Psalm 46:1 - God is our refuge and strength, an ever-present help in trouble.",
    "Jeremiah 29:11 - For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, plans to give you hope and a future.",
    "1 Peter 5:7 - Cast all your anxiety on him because he cares for you.",
    "Romans 15:13 - May the God of hope fill you with all joy and peace as you trust in him, so that you may overflow with hope by the power of the Holy Spirit.",
    "Psalm 34:17-18 - The righteous cry out, and the Lord hears them; he delivers them from all their troubles. The Lord is close to the brokenhearted and saves those who are crushed in spirit.",
    "Isaiah 40:31 - But those who hope in the Lord will renew their strength. They will soar on wings like eagles; they will run and not grow weary, they will walk and not be faint.",
    "Deuteronomy 31:6 - Be strong and courageous. Do not be afraid or terrified because of them, for the Lord your God goes with you; he will never leave you nor forsake you.",
    "Psalm 121:1-2 - I lift up my eyes to the mountains—where does my help come from? My help comes from the Lord, the Maker of heaven and earth.",
    "Hebrews 13:6 - So we say with confidence, 'The Lord is my helper; I will not be afraid. What can mere mortals do to me?'",
    "Psalm 9:9-10 - The Lord is a refuge for the oppressed, a stronghold in times of trouble. Those who know your name trust in you, for you, Lord, have never forsaken those who seek you.",
    "Psalm 37:4 - Take delight in the Lord, and he will give you the desires of your heart.",
    "Psalm 119:105 - Your word is a lamp for my feet, a light on my path.",
    "Romans 8:38-39 - For I am convinced that neither death nor life, neither angels nor demons, neither the present nor the future, nor any powers, neither height nor depth, nor anything else in all creation, will be able to separate us from the love of God that is in Christ Jesus our Lord.",
    "Isaiah 43:2 - When you pass through the waters, I will be with you; and when you pass through the rivers, they will not sweep over you.",
    "Psalm 16:8 - I keep my eyes always on the Lord. With him at my right hand, I will not be shaken.",
    "John 16:33 - In this world you will have trouble. But take heart! I have overcome the world.",
    "Psalm 27:1 - The Lord is my light and my salvation—whom shall I fear? The Lord is the stronghold of my life—of whom shall I be afraid?",
    "1 John 4:18 - There is no fear in love. But perfect love drives out fear.",
    "Psalm 118:6 - The Lord is with me; I will not be afraid. What can mere mortals do to me?",
    "2 Timothy 1:7 - For the Spirit God gave us does not make us timid, but gives us power, love and self-discipline."]
    counter_file = "print_counter.txt"
    counter = 0
    with open(counter_file, 'r') as f:
            counter = int(f.read())
    with open(counter_file, 'w') as f:
        f.write(str(counter+1))
    # print(counter)
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
            f"Today’s verse: {bible_verses[counter]}"
        )

        print(weather_message)
        # send_sms(weather_message, RECIPIENT_NUMBER, TEXTBELT_API_KEY)
    else:
        print("Failed to get weather data. SMS not sent.")

if __name__ == "__main__":
    main()
