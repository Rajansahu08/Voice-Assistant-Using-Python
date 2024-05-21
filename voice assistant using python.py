import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import smtplib
import requests
from pytube import YouTube, Search
import vlc
import os
from googletrans import Translator

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")  
    speak("I am Edith Sir. Please tell me how may I help you")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)  
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I didn't get that. Could you please repeat?")
        return "None"
    except sr.RequestError:
        print("Sorry, I'm having trouble accessing the Google API. Please check your internet connection.")
        return "None"

    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('slickkickks@gmail.com', 'ayush bhaiya')
    server.sendmail('singhtashu1911@gmail.com', to, content)
    server.close()

def getWeatherForecast(city):
    api_key = "a88c3c7821cf9a901d8ab9e7a15333e3"
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    complete_url = f"{base_url}?q={city}&appid={api_key}"
    response = requests.get(complete_url)
    data = response.json()

    forecast = ""
    for i in range(min(len(data["list"]), 1)):
        date = data["list"][i]["dt_txt"]
        temp = round(data["list"][i]["main"]["temp"] - 273.15, 1) 
        description = data["list"][i]["weather"][0]["description"]

        forecast += f"On {date}, the temperature in {city} is expected to be {temp}°C with {description}.\n"

    return forecast

def translateText(text, dest_language):
    translator = Translator()
    translated = translator.translate(text, dest=dest_language)
    return translated.text

if __name__ == "__main__":
    wishMe()
    instance = vlc.Instance()
    player = instance.media_player_new()

    songs = [
        r'C:\Users\91989\Desktop\Tinka-song.mp3',
        r'C:\Users\91989\Desktop\Dhundhala.mp3',
    ]
    current_song_index = 0

    while True:
        query = takeCommand().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=4)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
        elif 'play dhundhla song' in query:
            current_song_index = 1
            player.stop()  
            media = instance.media_new(songs[current_song_index])
            player.set_media(media)
            player.play()
        elif 'play tinka song' in query:
            current_song_index = 0
            player.stop() 
            media = instance.media_new(songs[current_song_index])
            player.set_media(media)
            player.play()
        elif 'pause' in query:
            player.pause()
            speak("Music paused.")
        elif 'play' in query:
            player.play()
            speak("Music resume.")
        elif 'next song' in query:
            current_song_index = (current_song_index + 1) % len(songs)
            player.stop() 
            media = instance.media_new(songs[current_song_index])
            player.set_media(media)
            player.play()
            speak("Playing next song.")
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif 'date' in query:
            currentDate = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Sir, today's date is {currentDate}")

        elif 'search on youtube' in query:
            query = query.replace("search on youtube", "")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        elif 'play on youtube' in query:
            query = query.replace("play on youtube", "")
            speak(f"Searching for {query} on YouTube...")
            search_results = Search(query)
            video_url = search_results.results[0].watch_url
            webbrowser.open(video_url)
        elif 'next video on youtube' in query:
            speak("Playing next video on YouTube...")
            search_results = Search(query)
            video_url = search_results.results[1].watch_url
            webbrowser.open(video_url, new=0)
        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "singhtashu1911@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!") 
            except Exception as e:
                print(e)
                speak("Sorry my friend. I am not able to send this email")
        elif 'weather forecast' in query:
            try:
                speak("City name?")
                city = takeCommand()
                forecast = getWeatherForecast(city)
                speak(forecast)
                print(forecast) 
            except Exception as e:
                print(e)
                speak("Sorry my friend. I am not able to fetch the weather forecast")
        elif 'translate' in query:
            try:
                speak("What should I translate?")
                text = takeCommand()
                speak("To which language?")
                dest_language = takeCommand()
                translated_text = translateText(text, dest_language)
                speak(translated_text)
                print(translated_text)
            except Exception as e:
                print(e)
                speak("Sorry my friend. I am not able to translate this text")
            