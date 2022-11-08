#---------- SETTINGS ----------#


database_path = r"D:\Coding\BirthdayCord\birthdays.json"  #Fichier .json obligatoire (si ça bug mets r"birthdays.json")

channel_id = 1038482178507558924  # L'ID du channel (for Midnight it's 1026534852637499442)

ping_role_id = 1038482779756822678  # L'ID du rôle à ping pour les annivs

prefix = "&&"



#---------- CODE ----------#

import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
import asyncio
import json
import string
from datetime import datetime, timedelta

chars = string.ascii_uppercase + string.digits

load_dotenv()

clear = lambda: os.system("cls || clear")
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')

with open(database_path, 'a+') as f:
    f.close()



#---------- DATABASE SETUP ----------#


class BirthdayDB():
    def get(self):
        if os.path.getsize(database_path) > 0:
            with open(database_path, "rb") as f:
                keys = json.loads(f.read())
                return keys
        else:
            return {}

    def getList(self):
        if os.path.getsize(database_path) > 0:
            with open(database_path, "rb") as f:
                keys = list(json.loads(f.read()).keys())
                return keys
        else:
            return []

    def add(self, key:str, id):
        keys = self.get()
        if key in keys:
            return False
        else:
            keys[id] = (key, False)
            self.save(keys)
            return True
    
    def remove(self, id:int):
        try:
            if os.path.getsize(database_path) > 0:
                keys = self.get()
                keys.pop(id)
                self.save(keys)
                return True
            else:
                return False
        except:
            return False

    def save(self, dict):
        with open(database_path, "w") as f:
            f.truncate(0)
            json.dump(dict, f, indent=4)

db = BirthdayDB()



#---------- BOT CODE ----------#

@bot.command(aliases=["anniv", "anniversaire", "bd"])
async def birthday(ctx, date):
    
    birthdays = db.get()

    try:
        anniv = str(date)
        if "/" not in anniv:
            await ctx.reply(":warning: **Erreur** : Veuillez suivre le format JJ/MM (exemple: 28/03 pour le 28 mars)")
            return
    except:
        await ctx.reply(":warning: **Erreur** : Veuillez suivre le format JJ/MM (exemple: 28/03 pour le 28 mars)")
        return

    if str(ctx.author.id) not in birthdays.keys():
        db.add(anniv, ctx.author.id)
        await ctx.reply(f"Date d'anniversaire ajoutée avec succès 🎉 (`{anniv}`)")
        return

    else:
        db.remove(ctx.author.id)
        db.add(anniv, ctx.author.id)
        await ctx.reply(f"Date d'anniversaire modifiée avec succès 🎉 (`{anniv}`)")

    print(f"[+] Added new birthday : {ctx.author}")
    
    

@bot.command()
@commands.is_owner()
async def remove(ctx):
    if db.remove(ctx.author.id):
        embed=discord.Embed(title="Remove", description=f"Vous avez été retiré de la liste avec succès.", color=0xFFFFFF)
        await ctx.reply(embed=embed)
        print(f"[+] Removed {ctx.author.id}'s birthday")
    else:
        embed=discord.Embed(title="Remove", description=f"Erreur: Vous n'êtes pas dans la liste.", color=0xFFFFFF)
        await ctx.reply(embed=embed)



@bot.event
async def on_ready():
    clear()
    print(f"Connecté en tant que {bot.user}")

    while True:
        await asyncio.sleep(57)
        data = db.get()
        data2 = db.get()

        now = datetime.now()
        ajd = now.strftime("%d/%m")
        heure = int(now.strftime("%H"))

        if heure == 18:
            for key in data:
                if data[key][0] in ajd:
                    if data[key][1] == False:
                        #joyyx anniv

                        print(key)
                        id = int(key)
                        channel = bot.get_channel(channel_id)
                        user = bot.get_user(id)
                        await user.send(f"Joyeux anniversaire ! :tada:")
                        await channel.send(f"<@&{ping_role_id}> C'est l'anniversaire de <@{id}> aujourd'hui ! :tada:")
                        data2[key][1] = True
                else:
                    data2[key][1] = False
                
        db.save(data2)

@bot.command(name="help")
async def help(ctx):
    helpmsg = f"""**Commandes**
```
{prefix}birthday <date> | Rajoute ton anniversaire à la liste ou le modifie.

{prefix}remove | Retire ton anniversaire de la liste.
```
```
{prefix}help | Voir ce message.
```"""

    embed=discord.Embed(title="Aide", description=helpmsg, color=0x000000)
    embed.set_footer(text="Dev par Epsi#0001 :)")
    await ctx.reply(embed=embed)

token = os.getenv("TOKEN")
bot.run(token)
