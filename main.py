# CIT 93 Final Program Project
# JAWA (Just Another Weather App)
# by: Mark Edmunds
# Date 11/2/2023
# This program will allow the user to enter a city and state and return the current weather conditions for that location.

# Import modules
from datetime import datetime
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
import math
import UserPreferences
from WeatherServices import WeatherServices
from kivy.uix.button import Button


class Weather(BoxLayout):
    tpo_menu = ObjectProperty(None)
    weather_output = ObjectProperty(None)
    city = ObjectProperty(None)
    daily_weather = ObjectProperty(None)
    current_weather = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def search_button_pressed(self, text_input):
        if text_input == "":
            self.top_menu.text_input.hint_text = "You must enter a city"
        else:
            print(f"Search button pressed {text_input}")
            forcast = WeatherServices.get_weather_for(text_input)
            self.weather_output = forcast["weather"]
            self.city = forcast["city"]
            self.top_menu.weather_response = self.weather_output
            self.output_weather()
            print(self.weather_output)

    def get_user_preferred_unints(self) -> str:
        units = UserPreferences.UserPreferences(**UserPreferences.UserPreferences.load()).units
        match units:
            case "metric":
                return str(chr(0x2103))
            case "imperial":
                return str(chr(0x2109))
            case _:
                raise ValueError("Invalid unit type")

    def output_weather(self):
        if self.weather_output == None:
            raise ValueError("No weather data to display")
        else:
            self.current_weather.current_city_label.text = self.city.name
            self.current_weather.current_temp_label.text = str(
                f"{math.floor(self.weather_output.current.temp)} {self.get_user_preferred_unints()}")
            self.current_weather.current_humidity_label.text = str(self.weather_output.current.humidity)
            self.current_weather.current_pressure_label.text = str(self.weather_output.current.pressure)
            self.current_weather.current_wind_label.text = str(self.weather_output.current.wind_speed)
            self.current_weather.current_visibility_label.text = str(self.weather_output.current.visibility)
            self.current_weather.current_sunrise_label.text = datetime.fromtimestamp(
                self.weather_output.current.sunrise).strftime("%H:%M")
            self.current_weather.current_sunset_label.text = datetime.fromtimestamp(
                self.weather_output.current.sunset).strftime("%H:%M")


            self.daily_weather.clear_widgets()
            for day in self.weather_output.daily:
                date = datetime.fromtimestamp(day.dt).strftime("%A, %d")
                view = DailyWeather()
                view.day_label = date.__str__()
                view.daily_temp_label = str(f"{math.floor(day.temp.max)}{self.get_user_preferred_unints()}")
                self.daily_weather.add_widget(view)



class DailyView(BoxLayout):
    """This class will display the daily weather forecast. Defined in the .kv file"""
    pass


class CurrentWeather(BoxLayout):
    current_weather_icon = ObjectProperty(None)
    current_temp_label = ObjectProperty(None)
    current_city_label = ObjectProperty(None)
    current_sunrise_label = ObjectProperty(None)
    current_sunset_label = ObjectProperty(None)
    current_humidity_label = ObjectProperty(None)
    current_wind_label = ObjectProperty(None)
    current_pressure_label = ObjectProperty(None)
    current_visibility_label = ObjectProperty(None)



class TopMenu(BoxLayout):
    text_input = ObjectProperty(None)
    weather_response = ObjectProperty(None)
    imperial = ObjectProperty(None)
    metric = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)



    def get_default_units(self,button):
        units = UserPreferences.UserPreferences(**UserPreferences.UserPreferences.load()).units
        if button == units:
            return "down"
        else:
            return "normal"

    def unit_button_pressed(self, unit):
        print(f"Unit button pressed {unit}")
        prefs = UserPreferences.UserPreferences(**UserPreferences.UserPreferences.load())
        match unit:
            case "metric":
                prefs.units = unit
                self.metric.state = "down"
            case "imperial":
                prefs.units = unit
                self.imperial.state = "down"

            case _:
                raise ValueError("Invalid unit type")
        prefs.save()


class DailyWeather(BoxLayout):
    day_label = StringProperty("")
    daily_weather_icon = StringProperty("sun.max.fill.png")
    daily_temp_label = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get_day_from_timestamp(timestamp):
        return datetime.fromtimestamp(timestamp).strftime("%A")


class CitySearch(TextInput):
    pass


class JAWAApp(App):
    def build(self):
        return Weather()


if __name__ == "__main__":
    JAWAApp().run()
