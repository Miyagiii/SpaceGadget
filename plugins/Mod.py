# Coded by TheSpaceCowboy
# Git: https://www.github.com/thespacecowboy42534
# Date: ‎21/8/17

#Imports
import discord,sys,sqlite3
from discord.ext import commands
from plugins.Helper import Helper

class Mod:
    """Mod stuff"""
    def __init__(self, bot):
        self.bot = bot
        self.spam = 0
        print('Addon "{}" loaded'.format(self.__class__.__name__))
        
    @commands.command(pass_context = True)
    async def get_id(self,ctx,user : discord.Member): # Gets ID's from user
        """Gets ID's from a user Syntax: s.get_ids [@user]"""
        if(await Helper.isPerms(self,ctx,2)): # Checks perms
           
           await self.bot.say(user.id) # Says the ID of the user
           await Helper.log(self,str(ctx.message.author),"get_ids "+user.name,str(ctx.message.timestamp)) # Logs command


    @commands.command(pass_context = True)
    async def give_role(self,ctx,user : discord.Member, role : int): # Gives role to user
        """Gives role to user. Syntax: s.giveRole [@user] [role]"""
        if(await Helper.isPerms(self,ctx,0) and user is not None): # If the perms are correct and user exists
            await Helper.giveRole(self,user,role) # Give the user the role
            await Helper.log(self,str(ctx.message.author),"give role "+str(role)+" to "+user.name,str(ctx.message.timestamp)) # Log command
    @commands.command(pass_context = True)
    async def get_role(self,ctx,user : discord.Member): # Gets user role
        """Gives role to user. Syntax: s.giveRole [@user] [role]"""
        if(await Helper.isPerms(self,ctx,0) and user is not None): # If the perms are correct and user exists
            level =await Helper.getRole(self,ctx,user.id)
            await self.bot.say(str(user.name)+": level "+str(level)) # Give the user the role
            await Helper.log(self,str(ctx.message.author),"get role of "+str(user.name)+" to "+user.name,str(ctx.message.timestamp)) # Log command

    @commands.command(pass_context = True)
    async def fixdb(self,ctx): # Incase of new joins while bot is down
        """If users joined while the bot was down it won't haveadded them to the database, this adds them to it. Syntax: s.fixdb"""
        if(await Helper.isPerms(self,ctx,1)):
            c = self.bot.conn.cursor() # Creates database cursor
            for users in ctx.message.author.server.members:
                print(users.display_name)
                c.execute('INSERT INTO users(name,uid,access,banned) VALUES(?,?,?,?)',(users.display_name,users.id,3,0))
            c.execute('DELETE FROM users WHERE rowid NOT IN (SELECT min(rowid) FROM users GROUP BY uid, name)') # Delete duplicate users with different wors
            self.bot.conn.commit()
            await self.bot.say("updated the database")
        
    @commands.command(pass_context = True)
    async def cleandb(self,ctx): # Incase of duplicate entries clean the database of duplicates
        """Removes duplicate entries into database. syntax: s.cleandb"""
        c = self.bot.conn.cursor() # Creates database cursor
        if(await Helper.isPerms(self,ctx,1)): # Checks permissions
            c.execute('DELETE FROM users WHERE rowid NOT IN (SELECT min(rowid) FROM users GROUP BY uid, name)') # Delete duplicate users with different wors
            self.bot.conn.commit() # Save Database
            await self.bot.say("Duplicates in database removed!") # Tells user duplicates a removed
            await Helper.log(self,str(ctx.message.author),"Cleandb",str(ctx.message.timestamp)) # Log command

    @commands.command(pass_context = True)
    async def ban(self,ctx,user : discord.Member): # Bans user from using the bot. Bot doesnt use server permissions and isn't supposed to be used for administration
        """Ban user from bot. Syntax: s.ban [@user]"""
        if(await Helper.isPerms(self,ctx,1)): # If you are a admin user on the bot
            await Helper.ban(self,ctx,user) # Ban the user from the bot
            await Helper.log(self,str(ctx.message.author),"Banned "+user.display_name,str(ctx.message.timestamp)) # Log command

    @commands.command(pass_context = True) 
    async def unban(self,ctx,user : discord.Member): # Unbans user from bot
        """Unbans user. Syntax: s.unban [@user]"""
        if(await Helper.isPerms(self,ctx,1)): # If the user is a bot admin
            await Helper.unban(self,user) # unban the user
    @commands.command(pass_context = True)
    async def get_servers(self,ctx): # Gets all servers
        """Gets server. Syntax: s.get_servers"""
        if(await Helper.isPerms(self,ctx,2)): # If the user is trusted get all servers. This command will eventually break without word wrap
            s = "" # placeholder for message
            await self.bot.send_message(ctx.message.author,"Servers:") # Gives a heading
            for servers in self.bot.servers: # Itterates through server list
                s += servers.name+"\t:\t"+servers.id+"\n" # Appends server name and id
            await self.bot.send_message(ctx.message.author,s) # Says message
    @commands.command(pass_context = True)
    async def load(self,ctx): # Loads module from path
        """Loads module. s.load [module path]"""
        if(await Helper.isPerms(self,ctx,1)): # If user is admin
            message = ctx.message.content.replace(self.bot.config['prefix']+"load ","") # Remove the message
            self.bot.load_extension(message) # Load the extension
            await self.bot.say("Module loaded sucessfully") # Alert the user that the extension was loaded sucessfully
            await Helper.log(self,str(ctx.message.author),"load "+message,str(ctx.message.timestamp)) # Logs command

    @commands.command(pass_context = True)
    async def unload(self,ctx): # Unload a module
        """Unloads module. s.unload [module path]"""
        if(await Helper.isPerms(self,ctx,1)): # If they are admin
            message = ctx.message.content.replace(self.bot.config['prefix']+"unload ","") # Remove the command
            self.bot.unload_extension(message) # Unload the extension
            await self.bot.say("Module unloaded sucessfully") # Alerts the user that module has been unloaded
            await Helper.log(self,str(ctx.message.author),"unload "+message,str(ctx.message.timestamp)) # Logs command
    @commands.command(pass_context = True)
    async def get_channels(self,ctx):
        """Gets channels. s.get_channels"""
        if(await Helper.isPerms(self,ctx,2)): # Gets channels
            await self.bot.send_message(ctx.message.author,"Channels:") # Sends header for command
            for channel in self.bot.get_all_channels(): # Gets all channels. This command broke really easily and i haven't added word wrap so I did it as individual messgae for now
                #TODO: word wrap
                s = str(channel.name)+"\t:\t"+str(channel.id)+"\t:\t"+str(channel.server) # Constructs the message
                await self.bot.send_message(ctx.message.author,s) # Sends message
            await self.bot.send_message(ctx.message.author,"end") # Lets the user now thats the end of the channel list
            await Helper.log(self,str(ctx.message.author),"Get channels",str(ctx.message.timestamp)) # Logs command

    @commands.command(pass_context = True)
    async def reload(self,ctx): # Relods bot
        """Reloads bot. Syntax: s.reload"""
 
        if(await Helper.isPerms(self,ctx,1)): # Checks if admin
            
            conf = Helper.readconf() # Re reads the config file
            self.bot.config = conf
            print("Reloading addons:") # Prints reloading addons
            Helper.unload_plugins(self.bot) # Unload all plugins
            
            Helper.load_plugins(self.bot) # Loads all plugins
            await self.bot.say("Reload Sucessful") # Says the reload was sucessful
            await Helper.log(self,str(ctx.message.author),"Reload",str(ctx.message.timestamp)) # Logs command


    @commands.command(pass_context = True)
    async def shutdown(self,ctx): # Shuts down the bot
        """Shuts down bot. syntax: s.shutdown"""
        if(await Helper.isPerms(self,ctx,0)): # Only owner can do this
            await self.bot.say("Goodbye!") # Says goodbyes
            await Helper.log(self,str(ctx.message.author),"Shutdown",str(ctx.message.timestamp)) # Logs command
            sys.exit("ShutdownSucessful") # Shuts down bot

            
def setup(bot):
    bot.add_cog(Mod(bot))
