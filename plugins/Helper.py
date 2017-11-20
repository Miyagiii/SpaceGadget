# Coded by TheSpaceCowboy
# Git: https://www.github.com/thespacecowboy42534
# Date: ‎19/8/17

#Imports
import discord,os,sys,json,sqlite3
from discord.ext import commands

class Helper:

    def __init__(self, bot):
        self.bot = bot
        bot.load_extension("Helper")
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    async def log(self,name,com,time):# Logs commands
        
        filename = "Discord.log" # Files name
        write = name+": used "+com+ " at "+time # Message
        
        for x in range(len(write)):print("#",end="") # This is used to outline the command
        print(end="\n") # Used to add an endpoint to the print function
        print(str(write.encode(sys.stdout.encoding, errors='replace'))) # Print the message, encoding is still an issue
        for x in range(len(write)):print("#",end="") # This is used to outline the command
        print(end="\n") # Used to add an endpoint to the print function
        
        if os.path.exists(filename):
            append_write = 'a' # Append if already exists
        else:
            append_write = 'w' # Make a new file if not

        #TODO: change this to a with statement for reduction in code
        writer = open(filename,append_write)# Opens the file we created and writes the log information into it
        writer.write(write+"\n") # Write to file
        writer.close() # Close file

    async def getRole(self,ctx,user : discord.Member): # Gets role from user
        c = self.bot.conn.cursor()
        c.execute('SELECT * FROM users WHERE uid = (?)',(user,)) # Gets id.
        access = 0
        for rows in c.fetchall():
            access = rows[3]
        return access
    async def ban(self,ctx,user : discord.Member):  #Ban system it works, but its backwards, might try and improve readability here
        c = self.bot.conn.cursor()
        access1 = await Helper.getRole(self,ctx,user.id) # Person being banned
        access2 = await Helper.getRole(self,ctx,ctx.message.author.id) # Person banning
        
        
        if(access2 < access1): # Compares the access levels if banner has lower access(which in my bot means higher access e.g. 0 = owner 1 = super user 2 = trusted 3 = user etc) which will resulton ban
            c.execute('UPDATE users SET banned = (?) WHERE uid = (?)',(1,user.id)) # Bans user
            await self.bot.say(user.name+" is successfully banned from the bot!")
        else: # Display error
            await self.bot.say("```Cannot ban a person of equal or higher ranked user than you!```")
        self.bot.conn.commit()
        c.close()



    async def unban(self,user : discord.Member): # Unbans user from bot
        c = self.bot.conn.cursor() # Creates a database cursor
        c.execute('SELECT * FROM users WHERE uid = (?) AND banned = 1',(user.id,))  # Executes a sql command
        if(len(c.fetchall()) == 1): # If anything at all is returned
            c.execute('UPDATE users SET banned = (?) WHERE uid = (?)',(0,user.id)) # Update the ban status
            await self.bot.say(user.name+" is successfully unbanned from the bot!") # Tells the user the unban was sucessful
        else:
            await self.bot.say(user.name+" is not banned") # Otherwise the user wasn't banned because he wasn't found
        self.bot.conn.commit() # Saves the database

    async def giveRole(self,user : discord.Member,role : int): # Gives roles
        c = self.bot.conn.cursor()
        c.execute('UPDATE users SET access = (?) WHERE uid = (?)',(role,user.id)) # Updates database
        await self.bot.say(user.name+" has been given access level "+str(role)) # Alerts users to new role
        self.bot.conn.commit() # Saves database


        
            
    def load_plugins(self): # Loads all extentions
        for extension in self.config['extensions']:# Gets all the extension locations from the json file
           try:
               self.load_extension(extension['name']) # Tries to load the file
           except Exception as e:
               print('{} failed to load.\n{}: {}'.format(extension['name'], type(e).__name__, e)) # If it fails it prints a message into console
    def unload_plugins(self): # Unloads all extentions
        for extension in self.config['extensions']: # Gets all the extension locations from the json
           try:
               self.unload_extension(extension['name']) # Trys to unload all the extensions from the json file
           except Exception as e:
               print('{} failed to load.\n{}: {}'.format(extension['name'], type(e).__name__, e)) # If it fails it prints a message into console
    def readconf(): # Reads config
        with open('config.json') as data:
            return json.load(data)   
            
    async def isBanned(self,ctx): # Checks bans
        c = self.bot.conn.cursor() # Creates a cursor
        user = str(ctx.message.author.id) # Gets the id from the context
        c.execute('SELECT * FROM users WHERE banned = 1 AND uid = (?)',(user,)) # Fetches a user with their id and a banned value
        if(len(c.fetchall()) > 0 ): # If it returns anything they are banned
            await self.bot.say("```BE GONE THOT, BANNED```")
            c.close()
            return True
        else: # They are not banned
            c.close()
            return False
        
    async def isPerms(self,ctx,req : int): # Checks permissions
        c = self.bot.conn.cursor() # Creates cursor
        user = str(ctx.message.author.id) # Gets user from context
        c.execute('SELECT * FROM users WHERE uid = (?) AND access <= (?)',(user,str(req))) # Gets a user with their id and access required

        if(len(c.fetchall()) > 0 ): # If anything is returned they are authorised
            c.close()
            return True
        else: # Otherwise they don't have high enough permissions
            await self.bot.say("```Insufficent access, {} access required```".format(str(req)))
            c.close()
            return False
        
    def createDB(self):
        c = self.conn.cursor() # Creates db cursor
        c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,name TEXT, uid TEXT,access INTERGER,banned INTERGER)') # Creates database if it doesn#t already exist
        c.execute('SELECT * FROM users') # Gets all users
        owner = "" # Creates placeholder for owner
        for user in self.config['owner']: # Gets the owner id
            owner = user['id']
        if(owner == "" or owner is None): # If the owner id isn't found json isn't setup correctly
            sys.exit("Json Not Configured Correctly please set an owner")
            
        c.execute('UPDATE users SET access = (?) WHERE uid = (?)',(0,owner)) # Adds owner
        self.conn.commit() # Saves db
        c.close() # Closes cursor

    async def wordWrap(sentence : str):
        arrayOfParagraphs = []
        r = "" # Is the result of the concatination of the words
        for letters in sentence: # This loops through every letter in the sentence
            r += letters
            if(len(r) > 1900): #When the amount of words is greater than 1900 then add a new paragraph (I chose this number for padding)
                arrayOfParagraphs.append(r+"[CONTINUE]")
                r = ""
                
        arrayOfParagraphs.append(r)# When the loops finished there might be a few letters or words left out the intial loop, this is just here to make sure the everything is displayed
    

        return arrayOfParagraphs
            
                
        


def setup(bot):
    bot.add_cog(Helper(bot))









