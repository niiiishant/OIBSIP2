import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import os

API_KEY = "5c55324d84bee64abec4b342a104d726"

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            city_name = data["name"]
            country = data["sys"]["country"]
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            wind_speed = data["wind"]["speed"]
            icon = data["weather"][0]["icon"]

            weather_info = f"City: {city_name}, {country}\nTemperature: {temp}°C\nWeather: {weather}\nWind Speed: {wind_speed} m/s"
            label_result.config(text=weather_info)

            icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
            response = requests.get(icon_url, stream=True)
            if response.status_code == 200:
                if not os.path.exists("icons"):
                    os.makedirs("icons")
                with open(f"icons/{icon}.png", "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                icon_image = Image.open(f"icons/{icon}.png")
                icon_photo = ImageTk.PhotoImage(icon_image)
                label_icon.config(image=icon_photo)
                label_icon.image = icon_photo  # Keep a reference to the photo
            else:
                print("Failed to download icon")

        else:
            messagebox.showerror("Error", "City not found")
    except Exception as e:
        messagebox.showerror("Error", f"An Error Occured: {e}")

def search_weather():
    city = entry_city.get()
    if city:
        get_weather(city)
    else:
        messagebox.showwarning("Input Error", "Please enter a city name")

root = tk.Tk()
root.title("Weather App")
root.geometry("1024x768")

background_image = Image.open("openweathermap.png")
width, height = background_image.size
new_width = 1024  # Set a fixed width for the background image
new_height = 768  # Set a fixed height for the background image
background_image = background_image.resize((new_width, new_height))
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.image = background_photo  # Keep a reference to the photo
background_label.place(x=0, y=0, relwidth=1, relheight=1)

label_city = tk.Label(root, text="Enter city:", bg="#fff", fg="#000")
label_city.place(relx=0.4, rely=0.1, anchor="center")

entry_city = tk.Entry(root, width=20)
entry_city.place(relx=0.4, rely=0.2, anchor="center")

button_search = tk.Button(root, text="Get Weather", command=search_weather, bg="#007bff", fg="#fff")
button_search.place(relx=0.4, rely=0.3, anchor="center")

label_result = tk.Label(root, text="", font=("Helvetica", 12), bg="#fff", fg="#000")
label_result.place(relx=0.4, rely=0.5, anchor="center")

label_icon = tk.Label(root, bg="#fff")
label_icon.place(relx=0.4, rely=0.6, anchor="center")

root.mainloop()
