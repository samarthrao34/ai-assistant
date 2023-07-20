import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    # Function to speak the given text
    engine.say(text)
    engine.runAndWait()

def wishMe():
    # Function to greet the user based on the time of day
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello, Good Morning")
        print("Hello, Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello, Good Afternoon")
        print("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")
        print("Hello, Good Evening")

def takeCommand():
    # Function to recognize user's speech using Google's Speech Recognition
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said: {statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement

def get_weather(city_name):
    # Function to get weather information based on city name and return temperature in Celsius
    api_key = "f6a690734dcf09dd837cf6fc8fd18f30"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        if "main" in x:
            y = x["main"]
            current_temperature = y["temp"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            speak("Temperature in Celsius is " +
                  str(current_temperature) +
                  "°C\nHumidity in percentage is " +
                  str(current_humidity) +
                  "%\nDescription: " +
                  str(weather_description))
            print("Temperature in Celsius = " +
                  str(current_temperature) +
                  "°C\nHumidity (in percentage) = " +
                  str(current_humidity) +
                  "%\nDescription = " +
                  str(weather_description))
        else:
            speak("Weather information not available for the given city.")
            print("Weather information not available for the given city.")
    else:
        speak("City Not Found")
        print("City Not Found")

def talk_with_assistant():
    # Function to enable general conversation with the assistant
    while True:
        speak("What would you like to talk about?")
        user_input = takeCommand().lower()

        if "goodbye" in user_input or "exit" in user_input or "stop" in user_input:
            speak("Goodbye! Have a great day!")
            print("Goodbye! Have a great day!")
            break

        if "how are you" in user_input:
            speak("I'm fine, thank you! How are you?")
            print("I'm fine, thank you! How are you?")
            # You can add more responses based on user input here

        elif "tell me a joke" in user_input:
            joke = "Why don't scientists trust atoms? Because they make up everything!"
            speak(joke)
            print(joke)

        # Add more conversational topics and responses here
        # Example:
        # elif "what's your favorite color" in user_input:
        #     speak("I'm just a computer program, so I don't have a favorite color.")
        #     print("I'm just a computer program, so I don't have a favorite color.")

        else:
            speak("I'm sorry, I don't have a response for that. Please ask something else.")
            print("I'm sorry, I don't have a response for that. Please ask something else.")

def main():
    speak("Loading your AI personal assistant Gojo")
    wishMe()

    while True:
        speak("Tell me how can I help you now?")
        statement = takeCommand().lower()
        if statement == 0:
            continue

        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak('your personal assistant Gojo is shutting down, Goodbye')
            print('your personal assistant Gojo is shutting down, Goodbye')
            break

        if 'wikipedia' in statement:
            # Search and speak the Wikipedia summary
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in statement:
            # Open YouTube in the web browser
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("YouTube is open now")
            time.sleep(5)

        elif 'open google' in statement:
            # Open Google in the web browser
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google Chrome is open now")
            time.sleep(5)

        elif 'open gmail' in statement:
            # Open Gmail in the web browser
            webbrowser.open_new_tab("https://mail.google.com")
            speak("Google Mail is open now")
            time.sleep(5)

        elif "weather" in statement:
            # Get weather information based on city name
            speak("What's the city name?")
            city_name = takeCommand()
            get_weather(city_name)

        elif 'time' in statement:
            # Get and speak the current time
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            # Speak about the assistant's capabilities
            speak('My name is Gojo, and I am Gojo version 1.0, your personal assistant. I am designed to handle various minor tasks, such as opening YouTube, Google Chrome, Gmail, and Stack Overflow. Additionally, I can predict time, capture photos, search Wikipedia, forecast weather in different cities, fetch top headline news from Times of India, and provide answers to computational or geographical questions!')

        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            # Speak about the creator of the assistant
            speak("I was built by Samarth")
            print("I was built by Samarth")

        elif "open stackoverflow" in statement:
            # Open Stack Overflow in the web browser
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is Stack Overflow")

        elif 'news' in statement:
            # Open Times of India's headlines in the web browser
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India. Happy reading!')
            time.sleep(6)

        elif "camera" in statement or "take a photo" in statement:
            # Capture a photo using the camera
            ec.capture(0, "robo camera", "img.jpg")

        elif 'search' in statement:
            # Perform a search on the web
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'talk with me' in statement or 'chat' in statement:
            # Enable general conversation with the assistant
            talk_with_assistant()

        elif 'ask' in statement:
            # Answer computational or geographical questions using Wolfram Alpha API
            speak('I can answer computational and geographical questions. What question do you want to ask now?')
            question = takeCommand()
            app_id = "E6X49R-5L8LA44QUV"  # Replace with your Wolfram Alpha API app_id
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)

        elif "log off" in statement or "sign out" in statement:
            # Log off the PC
            speak("Ok, your PC will log off in 10 seconds. Make sure you exit from all applications.")
            subprocess.call(["shutdown", "/l"])

if __name__ == '__main__':
    main()
    time.sleep(3)
