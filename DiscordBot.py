import discord
from discord.ext import commands, tasks
from itertools import cycle
import json
import requests
import os
from flask import Flask
from threading import Thread

client = commands.Bot(command_prefix='#')


####################
app = Flask('')

@app.route('/')
def home():
  return "Your Bot Is Online!"

def run():
  app.run(host='0.0.0.0', port=8000)

def keep_alive():
  serve = Thread(target=run)
  serve.start()
####################


####################
# Provinces are listed in an array in the API ranging from 0 to 12
# This dictionnary defines the provincial codes to their respective index value
indexConversions = {
    "ON": 0,
    "QC": 1,
    "NS": 2,
    "NB": 3,
    "MB": 4,
    "BC": 5,
    "PE": 6,
    "SK": 7,
    "AB": 8,
    "NL": 9,
    "NT": 10,
    "YK": 11,
    "NU": 12,
}

# Defines the provincial code to the proper provincial name 
# Used for printing
areaConversions = {
  "ON": "Ontario",
  "QC": "Québec",
  "NS": "Nova Scotia",
  "NB": "New Brunswick",
  "MB": "Manitoba",
  "BC": "British Columbia",
  "PE": "Prince Edward Island",
  "SK": "Saskatchewan",
  "AB": "Alberta",
  "NL": "Newfoundland and Labrador",
  "NT": "Northwest Territories",
  "YK": "Yukon",
  "NU": "Nunavut",
}
####################


####################
#Total Cases
@client.command(aliases = ['Cases', 'cases', 'case', 'Case', 'infected', 'Infected'])
async def total_cases(passed_context, *, area):
# Retrieves the cases for the input province
# Calls dictionnary indexConversions to get the appropriate array index for area 
  if area != 'Canada':
    data = "https://api.covid19tracker.ca/summary/split"
    write = requests.get(data)
    cases_province = write.json()['data'][indexConversions[area]]['total_cases']
    # Print the returned Covid-19 case value to the discord server
    # Call areaConversions to print out the full province name instead of the provincial code
    await passed_context.send(f'There have been {cases_province} total Covid-19 cases in {areaConversions[area]}')

# Retrieves the cases for Canada
# Canada is index 0 in the array for the API
  elif area == 'Canada':
    data = "https://api.covid19tracker.ca/summary"
    write = requests.get(data)
    cases_canada = write.json()['data'][0]['total_cases']
      
    await passed_context.send(f'There have been {cases_canada} total Covid-19 cases in Canada')
####################


####################
#Total Deaths
@client.command(aliases = ['Deaths', 'Death', 'Fatalities','TotalDeaths','deaths', 'death', 'fatalities'])
async def total_deaths(passed_context, *, area):
  if area != 'Canada':
    data = "https://api.covid19tracker.ca/summary/split"
    write = requests.get(data)
    deaths_province = int(write.json()['data'][indexConversions[area]]['total_fatalities'])
    cases_province = int(write.json()['data'][indexConversions[area]]['total_cases'])

    
    await passed_context.send(f'There have been {deaths_province} total Covid-19 deaths in {areaConversions[area]}, that is {round((deaths_province/cases_province)*100, 2)}% of total Covid-19 cases in {areaConversions[area]}')

  elif area == 'Canada':
    data = "https://api.covid19tracker.ca/summary"
    write = requests.get(data)
    deaths_canada = int(write.json()['data'][0]['total_fatalities'])
    cases_canada = int(write.json()['data'][0]['total_cases'])

    await passed_context.send(f'There have been {deaths_canada} total Covid-19 deaths in Canada, that is {round((deaths_canada/cases_canada)*100, 2)}% of total Covid-19 cases in Canada')
####################


####################
#Total Vaccinations
@client.command(aliases = ['TotalVaccinations','Vaccinations', 'VaccineAdministered', 'totalvaccinations', 'Totalvaccinations', 'vaccineadministered'])
async def vaccinations(passed_context, *, area):
  if area != 'Canada':
    data = "https://api.covid19tracker.ca/summary/split"
    write = requests.get(data)
    vaccinations_province = write.json()['data'][indexConversions[area]]['total_vaccinations']
    if vaccinations_province == 0:
      await passed_context.send(f'I could not find sufficient information to tell you the total number of vaccinations administered in {areaConversions[area]}')
    else: 
      await passed_context.send(f'There have been {vaccinations_province} total Covid-19 vaccinations administered in {areaConversions[area]}')

  elif area == 'Canada':
    data = "https://api.covid19tracker.ca/summary"
    write = requests.get(data)
    vaccinations_canada = write.json()['data'][0]['total_vaccinations']
      
    await passed_context.send(f'There have been {vaccinations_canada} total Covid-19 vaccinations administered in Canada')
####################


####################
#Total Vaccinated
@client.command(aliases = ['Vaccinated'])
async def vaccinated(passed_context, *, area):
  if area != 'Canada':
    # Retrieves the number of vaccinated for the input province
    data = "https://api.covid19tracker.ca/summary/split"
    write = requests.get(data)
    vaccinated_province = write.json()['data'][indexConversions[area]]['total_vaccinated']
    
    #Retrieves the population for the input province
    data_prov = "https://api.covid19tracker.ca/provinces"
    write_prov = requests.get(data_prov)
    population_province = write_prov.json()[indexConversions[area]]['population']

    # Call the following "if statement" if the value of vaccinated in a province is 0
    # This indicates that there is no updated information on the API for this province
    if vaccinated_province == 0:
      await passed_context.send(f'I could not find sufficient information to tell you the total number of vaccinated people in {areaConversions[area]}')
    # Calculates the pourcentage of vaccinated people in the input province
    else: 
      await passed_context.send(f'{vaccinated_province} people in {areaConversions[area]} have been vaccinated, that is {round((vaccinated_province/population_province)*100, 2)}% of people in {areaConversions[area]}')

  elif area == 'Canada':
    
    population_canada = 0
    data_prov = "https://api.covid19tracker.ca/provinces"
    write_prov = requests.get(data_prov)
    # In the API, the provinces range from indices 0 to 12
    # Loops through the API's array and calculates the sum of the provinces populations
    # Returns total population of Canada
    for i in range(12):
      pop_province = int(write_prov.json()[i]['population'])
      population_canada += pop_province
  
    data = "https://api.covid19tracker.ca/summary"
    write = requests.get(data)
    vaccinated_canada = int(write.json()['data'][0]['total_vaccinated'])
    
    await passed_context.send(f'{vaccinated_canada} people in Canada have been vaccinated, that is {round((vaccinated_canada/population_canada)*100, 2)}% of people in Canada')
####################


####################
#Total Boosters
@client.command(aliases = ['Boosters'])
async def boosters(passed_context, *, area):
  if area != 'Canada':
    data = "https://api.covid19tracker.ca/summary/split"
    write = requests.get(data)
    boosters_province = int(write.json()['data'][indexConversions[area]]['total_boosters_1'])

    data_prov = "https://api.covid19tracker.ca/provinces"
    write_prov = requests.get(data_prov)
    population_province = int(write_prov.json()[indexConversions[area]]['population'])

    if boosters_province == 0:
      await passed_context.send(f'I could not find sufficient information to tell you the total Covid-19 vaccine boosters administered in {areaConversions[area]}')
    else: 
      await passed_context.send(f'{boosters_province} people in {areaConversions[area]} have been administered the Covid-19 vaccination booster, that is {round((boosters_province/population_province)*100, 2)}% of people in {areaConversions[area]}')


  elif area == 'Canada':
    data = "https://api.covid19tracker.ca/summary"
    write = requests.get(data)
    boosters_canada = int(write.json()['data'][0]['total_boosters_1'])

    population_canada = 0
    data_prov = "https://api.covid19tracker.ca/provinces"
    write_prov = requests.get(data_prov)
    for i in range(12):
      pop_province = int(write_prov.json()[i]['population'])
      population_canada += pop_province
      
    await passed_context.send(f'{boosters_canada} people in Canada have been administered the Covid-19 vaccination booster, that is {round((boosters_canada/population_canada)*100, 2)}% of people in Canada')
####################


####################
status = cycle(['Thinking', 'Researching', 'Lunch Break'])
# Constant background tasks for the bot to continously updating
@tasks.loop(seconds=45)
async def background_change_status():
  await client.change_presence(activity=discord.Game(next(status)))
####################


####################
# Clears previous messages in the discord server
# Clears the specified amount of messages, or 100 messages if no amount is specified by user
@client.command()
async def clear(ctx, amount=100):
  await ctx.channel.purge(limit=amount)

#Other
@client.event
async def on_ready():
    print('Bot is logged in as {0.user}'.format(client))
    background_change_status.start()

@client.event
async def on_member_join(member_username):
  print(f'{member_username} has joined a server.')

@client.event
async def on_member_remove(member_username):
    print(f'{member_username} has left a server.')
####################

####################
# Run bot continuously
keep_alive()
TOKEN = os.environ.get('TOKEN')
client.run(TOKEN)
