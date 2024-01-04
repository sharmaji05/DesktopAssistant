from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import speech_recognition as sr
import time
import pyttsx3
import requests
import webbrowser

driver = webdriver.Edge()
driver.maximize_window()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

engine.say('Hi! i am your voice assistant')
engine.runAndWait()

recognizer = sr.Recognizer()
microphone = sr.Microphone()

def speak(query):
    engine.say(query)
    engine.runAndWait()


def recognize_speech():
    with microphone as source:
        audio = recognizer.listen(source, phrase_time_limit=5)
    response = ""
    speak("Identifying your words..")
    try:
        response = recognizer.recognize_google(audio)
    except:
        response = "Error"
    return response

def get_weather(city):
    api_key = 'YOUR_OPENWEATHERMAP_API_KEY'
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}  # You can change units to 'imperial' for Fahrenheit

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data['cod'] == '404':
            return "City not found. Please try again."

        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        weather_info = f"The current temperature in {city} is {temperature}°C. The weather is {description}."
        return weather_info
    except Exception as e:
        return f"Error fetching weather information: {str(e)}"

time.sleep(1)
speak("Hello Sir! i am now available..")
while True:
    speak("How may I help you? ")
    voice = recognize_speech().lower()
    print(voice)
    if 'open google' in voice:
        speak('Opening google')
        driver.execute_script("window.open('');")
        window_list = driver.window_handles
        driver.switch_to.window(window_list[-1])
        driver.get('https://google.com')
        
    elif 'search google' in voice:
        speak("I am listening. What do you want to search on Google?")
        query = recognize_speech()
        if query != 'Error':
            google_url = f'https://www.google.com/search?q={query}'
            webbrowser.open_new_tab(google_url)
            speak(f"Here are the search results for {query} on Google.")
    
    elif "hello" in voice:
        speak("Hey! how are you")
    
    elif "i am fine" in voice:
        speak("ohk that's good!.. everyone should be fine")
    
        
    elif 'open youtube' in voice:
        speak('Youtube is opening')
        driver.execute_script("window.open('');")
        window_list = driver.window_handles
        driver.switch_to.window(window_list[-1])
        driver.get('https://youtube.com')
    elif 'search youtube' in voice:
        while True:
            speak("I am listening")
            query = recognize_speech()
            if query != 'Error':
                break
        element = driver.find_elements('name','search_query')

        if element:
            first_element = element[0]
            first_element.send_keys(query)
            first_element.send_keys(Keys.RETURN)
    
    elif 'open application' in voice:
         speak("To open the app just say open appname")
         query = recognize_speech()
         from AppOpener import open, close
         def main():
               if "close " in query:
                   app_name = query.replace("close ","").strip()
                   close(app_name, match_closest=True, output=False)
               if "open " in query:
                   speak("Wait..App is opening ")
                   app_name = query.replace("open ","")
                   open(app_name, match_closest=True)
         main()

    elif 'open twitter' in voice:
        speak('Opening Twitter')
        driver.execute_script("window.open('');")
        window_list = driver.window_handles
        driver.switch_to.window(window_list[-1])
        driver.get('https://twitter.com')

    elif 'open facebook' in voice:
        speak('Opening Twitter')
        driver.execute_script("window.open('');")
        window_list = driver.window_handles
        driver.switch_to.window(window_list[-1])
        driver.get('https://facebook.com')

    elif 'open instagram' in voice:
        speak('Opening Twitter')
        driver.execute_script("window.open('');")
        window_list = driver.window_handles
        driver.switch_to.window(window_list[-1])
        driver.get('https://instagram.com')

    elif 'switch tab' in voice:
        num_tabs = len(driver.window_handles)
        cur_tab = 0
        for i in range(num_tabs):
            if driver.window_handles[i] == driver.current_window_handle:
                if i != num_tabs - 1:
                    cur_tab = i + 1
                    break
        driver.switch_to.window(driver.window_handles[cur_tab])

    elif 'what the time' in voice:
        current_time = time.strftime("%H:%M")
        speak(f"The current time is {current_time}")

    elif 'what the date' in voice:
        current_date = time.strftime("%Y-%m-%d")
        speak(f"The current date is {current_date}")

    elif 'today weather' in voice:
        speak("Sure, please specify the city.")
        city = recognize_speech()
        weather_info = get_weather(city)
        speak(weather_info)
        google_url = f'https://www.google.com/search?q={city} weather'
        webbrowser.open_new_tab(google_url)

    elif 'close tab' in voice:
        speak('Closing tab')
        driver.close()
    elif 'go back' in voice:
        driver.back()
    elif 'go forward' in voice:
        driver.forward()
    elif 'stop' in voice:
        driver.stop_casting()
    elif 'exit' in voice:
        speak('Goodbye sir!..I am going but any time you can call me') 
        driver.quit()
        break
    else:
        speak('Please speak your words clear')
    time.sleep(2)