import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive



client = discord.Client()


sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!"
]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")

  json_data = json.loads(response.text)
  quote =  json_data[0]["q"] 
  return(quote)

def get_fact():
  response = requests.get("https://useless-facts.sameerkumar.website/api")

  json_data = json.loads(response.text)
  fact =  json_data["data"] 
  return(fact)


def get_setup():
  response = requests.get("https://official-joke-api.appspot.com/random_joke")

  json_data = json.loads(response.text)
  setup =  json_data["setup"] 
  return(setup)

def get_punch():
  response = requests.get("https://official-joke-api.appspot.com/random_joke")

  json_data = json.loads(response.text)
  punchline =  json_data["punchline"] 
  return(punchline)  

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements



  
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))  

@client.event 
async def on_message(message):
  if message.author == client.user:
      return
  msg= message.content

  if message.content.startswith('$joke'):
      punchline = get_punch()
      setup = get_setup() 
      await message.channel.send(setup)
      await message.channel.send(punchline)




  if message.content.startswith('$fact'): 
    fact = get_fact()
    await message.channel.send('Hello @{.author}!'.format(message))
    await message.channel.send(fact)   

  if msg.startswith('$inspire'):
    quote= get_quote()
    await message.channel.send(quote)
  
  
  options = starter_encouragements
  if "encouragements" in db.keys():
      options = options + list(db["encouragements"])

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

   


      
keep_alive()
client.run(os.getenv('token'))