# Coded by TheSpaceCowboy
# Git: https://www.github.com/thespacecowboy42534
# Date: ‎01/9/17

#Imports
import discord,os,sys,json,sqlite3,random
from discord.ext import commands
from plugins.Helper import Helper
from plugins.General import General

class Error:

    def __init__(self, bot): # Initialisation of class
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
 
    async def on_command_error(self, ecx, ctx): # Error handling
        
        if(isinstance(ecx, commands.errors.CommandNotFound)): # Replies if an invalid command is input
            await self.bot.send_message(ctx.message.channel, "```I'm sorry but wtf are you talking about?```") 
        elif( isinstance(ecx, discord.ext.commands.errors.BadArgument)): # If an arguement is missing tell the user to type s.help for command usage
            await self.bot.send_message(ctx.message.channel, "```It appears as though you input some bad arguements, read help for usage of the command you attempted to use.```")    
        else: # If its unaccounted for print out issue, if this happens send log to me please.
            await self.bot.send_message(ctx.message.channel, ecx) 
            print(ecx)


       
    async def on_server_join(self,server):# When a bot joins a server update database
        c = self.bot.conn.cursor()
        print("joined:",server.name)
        for members in server.members:
            c.execute('INSERT INTO users(name,uid,access,banned) VALUES(?,?,?,?)',(members.display_name,members.id,3,0))
        self.bot.conn.commit()
        c.close()        

    async def on_message(self,message): # Cool easter eggs
        if(message.author.id == str(292007112660484097)):
            await self.bot.send_message(message.channel,"https://media.discordapp.net/attachments/340408579448242176/368848350537187328/loli_police.gif")
        if(message.content.find("?????") != -1 ):
            await self.bot.send_message(message.channel,"https://cdn.discordapp.com/attachments/311184555841290241/369205527122542592/1502191177039.png")
        if(message.content.find("Omae wa mou shindeiru") != -1 ):
           await self.bot.send_message(message.channel,"Nani?")
        if(message.author.id == str(283296102269190145)):
            await self.bot.send_message(message.channel,"https://media.discordapp.net/attachments/340408579448242176/368848350537187328/loli_police.gif")
        if(message.content.lower().find("nullpo") != -1 or message.content.lower().find("null po") != -1):
           await self.bot.send_message(message.channel,"Gah!")
        if(message.content.lower().find("mad scientist") != -1 or message.content.lower().find("madscientist") != -1):
            with open("./memes/Science/"+str(random.choice(os.listdir("./memes/Science/"))), 'rb') as f:
                await self.bot.send_file(message.channel, f)
        if(message.content.lower().find("hahaha") != -1):
            with open("./memes/haha/"+str(random.choice(os.listdir("./memes/haha/"))), 'rb') as f:
                await self.bot.send_file(message.channel, f)
        if(message.content.lower().find("loli") != -1 or message.content.lower().find("pony") != -1):
            with open("./memes/Digi/"+str(random.choice(os.listdir("./memes/Digi/"))), 'rb') as f:
                await self.bot.send_file(message.channel, f)
        if(message.content.lower().find("frau") != -1):
            with open("./memes/Frau/"+str(random.choice(os.listdir("./memes/Frau/"))), 'rb') as f:
                await self.bot.send_file(message.channel, f)                
        if(message.content.lower().find("creamed") != -1):
            with open("./memes/Creamed/"+str(random.choice(os.listdir("./memes/Creamed/"))), 'rb') as f:
                await self.bot.send_file(message.channel, f)      
        if(message.content.lower().find("cpu2") != -1):
            pronouns = ["him","her"]
            await self.bot.send_message(message.channel,random.choice(pronouns))

    async def on_member_update(self,before,after): # If a user changes their name update this in the database
        if(before.name != after.name):
            try:
                print(str(before.name.encode(sys.stdout.encoding), errors='replace')+" was updated to {}".format(after.name.encode(sys.stdout.encoding, errors='replace')))
            except:
                pass
            c = self.bot.conn.cursor()
            c.execute('SELECT * FROM users')
            c.execute('UPDATE users SET name = (?) WHERE uid = (?)',(after.name,after.id))
            self.bot.conn.commit()
            c.close()
    async def on_member_join(self,member): # If a member joins add them to the database
        print(str(member.name.encode(sys.stdout.encoding), errors='replace')+" joined :)")
        c = self.bot.conn.cursor()
        c.execute('INSERT INTO users(name,uid,access,banned,likes) VALUES(?,?,?,?,0)',(member.display_name,member.id,3,0))
        self.bot.conn.commit()
        c.close()
def setup(bot):
    bot.add_cog(Error(bot))









