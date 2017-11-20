# Coded by TheSpaceCowboy
# Git: https://www.github.com/thespacecowboy42534
# Date: ‎23/8/17

# Imports
import discord,random,json
from discord.ext import commands
from plugins.Helper import Helper
from Pymoe import Kitsu
from Pymoe import Anilist


class Anime:#Anime class
    """Stuff to do with anime"""
    
    def __init__(self, bot):
        
        self.bot = bot
        
        print('Addon "{}" loaded'.format(self.__class__.__name__))
        
    @commands.command(pass_context = True)
    async def ganime(self,ctx): # Gets anime from gogoanime
        """Gets anime from gogoanime syntax: prefix.ganime [name] optional:[Episode]"""
        
        if(await Helper.isBanned(self,ctx)):# Checks bans
            return
        
        if(await Helper.isPerms(self,ctx,3)):# Checks permissions - check helper for information on how that works

            phrase = ctx.message.content.lower().replace(self.bot.config["prefix"]+"ganime ", "")# Allows message to have multiple arguements without spliting the string into individual words
            phrase = phrase.replace(" ","-")#Stops spaces in the url
            
            if(phrase.lower().find("episode-") == -1):# Checks if user looked for an episode or not
                await self.bot.say("https://gogoanime.io/category/"+phrase)
            else:
                await self.bot.say("https://gogoanime.io/"+phrase)
                
            await Helper.log(self,str(ctx.message.author),"ganime "+phrase,str(ctx.message.timestamp))# Log file

    @commands.command(pass_context = True)
    async def asearch(self,ctx): # Gets anime info
        """Gets anime info syntax: s.asearch [name]"""
    
        if(await Helper.isBanned(self,ctx)): # Checks bans
            return
        
        if(await Helper.isPerms(self,ctx,3)): # Checks permissions
            
            instance = Kitsu("dd031b32d2f56c990b1425efe6c42ad847e7fe3ab46bf1299f05ecd856bdb7dd","54d7307928f63414defd96399fc31ba847961ceaecef3a5fd93144e960c0e151") # Creates kitsu instance with public key
            term = ctx.message.content.replace(self.bot.config["prefix"]+"asearch ","") # Gets search term
            anime = instance.anime.search(term) # Uses kitsu to find anime
            await self.bot.say(":thinking:")
            if(anime is None):  # If the anime isn't found let them know
                await self.bot.say("I can't find it most likely due to your terrible spelling, try not being an idiot next time.") 
                return
            
            anime = anime[0] # Returns a dictionary, need to select the 0th object to get all the information it got from the search
            showType = anime['type'] # Returns show type
            anime = anime['attributes'] # Grabs all data about the anime returned
            seriesType = anime['subtype'] # Returns if it's a show or movie
            title = anime['canonicalTitle']+" ("+showType+")" # Animes title 
            author = self.bot.user # Just used for embed data
            image = str(anime['posterImage']['original']) # Returns Image poster
            showStatus = anime['status'] # Get if the show has ended
            if(anime['startDate'] is None or anime['endDate'] is None): # If show hasn't begun or ended then it's TBA 
                aired = "TBA"
            else:
                aired = anime['startDate']+" - "+anime['endDate'] # If it started and ended then set the values
            episodes = anime['episodeCount'] # Returns episode count
            age = anime['ageRating'] # Returns age rating
            
            embed = discord.Embed(title=title,description=anime['synopsis'],colour = 0x206694) # Display's the synopsis with all relivent data in the embed
            embed.add_field(name="Ratings", value=anime["averageRating"]) 
            embed.add_field(name="Type:", value=seriesType)
            embed.add_field(name="Status:", value=showStatus)
            embed.add_field(name="Aired:", value=aired)
            embed.add_field(name="Episodes:", value=episodes)
            embed.add_field(name="AgeRating:", value=age)
            embed.set_image(url=image)
            embed.set_author(name=author.name,icon_url=author.avatar_url)
            await self.bot.say(embed = embed)
            
            await Helper.log(self,str(ctx.message.author),"asearch "+term,str(ctx.message.timestamp))

    @commands.command(pass_context = True)
    async def msearch(self,ctx): # Gets manga info
        """Gets manga info syntax: s.msearch [name]"""
        
        await self.bot.say(":thinking:")
        
        if(await Helper.isBanned(self,ctx)): # Checks bans
            return

        if(await Helper.isPerms(self,ctx,3)): # Checks perms
            
            instance = Kitsu("dd031b32d2f56c990b1425efe6c42ad847e7fe3ab46bf1299f05ecd856bdb7dd","54d7307928f63414defd96399fc31ba847961ceaecef3a5fd93144e960c0e151") # Creates kitsu instance
            term = ctx.message.content.replace(self.bot.config["prefix"]+"msearch ","") # Gets search term
            manga = instance.manga.search(term) # Searches term using kitsu instance
    
            if(manga is None): # If manga isn't found, display friendly message
                await self.bot.say("I can't find it most likely due to your terrible spelling, try not being an idiot next time.") 
                return
            
            manga = manga[0] # Returns dictionary so 0th object needs to be selected
            showType = manga['type'] # Gets manga type
            manga = manga['attributes'] # Gets all attribues for the returned manga
            seriesType = manga['subtype'] # Get's manga sub type if any
            title = manga['canonicalTitle']+" ("+showType+")" # Gets manga title
            author = self.bot.user # Name for embed
            image = str(manga['posterImage']['original']) # Gets poster for manga
            showStatus = manga['status'] # Gets manga status(TBA, ongoing etc)
            if(manga['startDate'] is None or manga['endDate'] is None): # If show hasn't begun or ended then it's TBA
                aired = "TBA"
            else:
                aired = manga['startDate']+" - "+manga['endDate'] # Display's start and end date if it has finished
                
            episodes = manga['chapterCount'] # Display's chapter Count
            age = manga['ageRating'] # gets age
            
            embed = discord.Embed(title=title,description=manga['synopsis'],colour=0xe74c3c) # Display's all data
            embed.add_field(name="Ratings(Kitsu)", value="#"+str(manga["ratingRank"]))
            embed.add_field(name="Type:", value=seriesType)
            embed.add_field(name="Status:", value=showStatus)
            embed.add_field(name="Aired:", value=aired)
            embed.add_field(name="Chapters:", value=episodes)
            embed.add_field(name="AgeRating:", value=age)
            embed.set_image(url=image)
            embed.set_author(name=author.name,icon_url=author.avatar_url)
            await self.bot.say(embed = embed)
            
            await Helper.log(self,str(ctx.message.author),"msearch "+term,str(ctx.message.timestamp)) # Logs command

   
        
    @commands.command(pass_context = True)
    async def csearch(self,ctx): # Gets info for character
        """Gets anime character info syntax: s.csearch [name]"""
        
        await self.bot.say(":thinking:")

        if(await Helper.isBanned(self,ctx)): # Checks bans
            return
        
        if(await Helper.isPerms(self,ctx,3)): # Checks perms
            ID = self.bot.config['anilist'][0]['client-name'] # Gets api key from json
            secret = self.bot.config['anilist'][1]['client-secret'] # Gets api key from json
            instance = Anilist(ID,secret) # Creates anilist instance using an input key
            term = ctx.message.content.replace(self.bot.config["prefix"]+"csearch ","") # Gets the term
            person = instance.search.character(term) # uses Anilist instance to search term
            
            if(person is None): # If character isn't found display message
                await self.bot.say("I can't find it most likely due to your terrible spelling, try not being an idiot next time.") 
                return
            
            person = person[0] #  Person is equal to the 0th term in the dictionary
            title = person['name_alt'] # Sets title to their nickname or alias e.g. Okabe = Hououin
            desc = person['info'] # The description is equal to their information
            image = person['image_url_med'] # Display's a picture of the character
            embeds = []  # Stores multiple embeds
            finished = False # Sets finished to false

            #TODO: make wordwrap function to stop reuse
            while finished == False: # This loop is to bypass the 2000 word limit allowed by discord, I do this by spliting the description into seperate embeds
                r = "" # Is the result of the concatination of the words
                for letters in desc: # This loops through every letter in the sentence
                    r += letters
                    if(len(r) > 1900): #When the amount of words is greater than 1900 then add a new embed (I chose this number for padding)
                        embeds.append(discord.Embed(title=title,description=r+"[CONTINUE]"),colour=0x2ecc71)
                        r = ""
                        
                embeds.append(discord.Embed(title=title,description=r,colour=0x2ecc71)) # When the loops finished there might be a few letters or words left out the intial loop, this is just here to make sure the everything is displayed
                embeds[0].set_image(url=image)
            
                finished = True # Ends loop
                
            for x in range(0,len(embeds)): # Prints all embeds
                await self.bot.say(embed=embeds[x])

            await Helper.log(self,str(ctx.message.author),"csearch "+term,str(ctx.message.timestamp)) # Logs command


                
       
    @commands.command(pass_context = True)
    async def kanime(self,ctx): # Gets anime from kissanime
        """Gets anime from kissanime syntax: s.kanime [name]"""
        
        if(await Helper.isBanned(self,ctx)): # Checks ban
            return
        
        if(await Helper.isPerms(self,ctx,3)): # Checks permissions
            phrase = ctx.message.content.lower().replace(self.bot.config["prefix"]+"kanime ", "") # Gets the search phrase
            phrase = phrase.replace(" ","-") # Replaces spaces with "-" because 'its a url
            await self.bot.say("http://kissanime.ru/Anime/"+phrase) # Display's link    
            await Helper.log(self,str(ctx.message.author),"kanime "+phrase,str(ctx.message.timestamp)) # Logs command


    @commands.command(pass_context = True)
    async def aanime(self,ctx): # Gets anime from anime streams
        """Gets anime from anime streams syntax: s.aanime [name]"""
        
        if(await Helper.isBanned(self,ctx)): # Checks ban status
            return
        
        if(await Helper.isPerms(self,ctx,3)): # Checks permissions
            phrase = ctx.message.content.lower().replace(self.bot.config["prefix"]+"aanime ", "") # Gets the search phrase
            phrase = phrase.replace(" ","-") # Replaces spaces with "-" because it's a url
            await self.bot.say("https://animestreams.tv/watch-"+phrase+"-full-episodes/") # Display's link
            await Helper.log(self,str(ctx.message.author),"aanime "+phrase,str(ctx.message.timestamp)) # Logs command   


def setup(bot):
    
    bot.add_cog(Anime(bot)) # Adds cog to bot
