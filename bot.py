#Weatherbot:
#It will will give local time in 24 hour format and 12 hour format.
#It will give weather in degree celcius and fahreheit.
#It will give the feels like weather in degree celcius and fahrenheit.
#It will give the weather conditions of the loaction.
#It will give the icon of the weather conditions.
#It will give a a map of the location.

import hikari 
import lightbulb  
import requests

bot = lightbulb.BotApp(token='TOKEN', intents=hikari.Intents.GUILD_MESSAGES)

def to_fahrenheit(degrees):
    result = degrees * 9/5 + 32
    return result

def convert_to_12hr(time_24hr):
    hours, minutes = map(int, time_24hr.split(':'))
    period = 'AM' if hours < 12 else 'PM'
    hours = hours % 12 if hours % 12 != 0 else 12
    time_12hr = f"{hours:02d}:{minutes:02d} {period}"
    return time_12hr

@bot.command()
@lightbulb.option('location', 'enter city, state or zip code',type=str)
@lightbulb.command('weather', 'responds with current weather')
@lightbulb.implements(lightbulb.SlashCommand)
async def get_weather(ctx):

    payload = {
  'access_key': 'KEY',
  'query': ctx.options.location
    }

    weather_req = requests.get('http://api.weatherstack.com/current', payload)
    response = weather_req.json()

    time = response['location']['localtime'].split()
    date = response['location']['localtime'].split()
    icon = response['current']['weather_icons']
    lon = response['location']['lon']
    lat = response['location']['lat']

    weather_embeds = [hikari.Embed(
        title = f"{response['location']['name']}, {response['location']['region']}:",
        description = f"""
        **Local Time:** {time[1]} or {convert_to_12hr(time[1])}
        **Temperature:** {to_fahrenheit(response['current']['temperature'])}°F or {(response['current']['temperature'])}°C
        **Feels Like:** {to_fahrenheit(response['current']['feelslike'])}°F or {(response['current']['feelslike'])}°C
        **Weather Description**: {response['current']['weather_descriptions'][0]}
        """,
        color = "#FF00FF"
        ), hikari.Embed(
            color = "#FF00FF"
        )]


    weather_embeds[0].set_image(icon[0])

    weather_embeds[1].set_image(f'https://api.mapbox.com/styles/v1/mapbox/dark-v10/static/{lon},{lat},11.49,0/600x600?access_token=TOKEN')
    weather_embeds[1].set_footer(f"Accessed at {date[0]}")
    
    await ctx.respond(embeds = weather_embeds)
        

bot.run() 