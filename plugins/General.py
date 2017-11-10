# Coded by TheSpaceCowboy
# Git: https://www.github.com/thespacecowboy42534
# Date: ‎19/8/17

#Imports
import discord,random,wikipedia,json,requests,os
from discord.ext import commands
from plugins.Helper import Helper
import giphypop
from giphypop import translate
import random as rNumber
import nltk
class General:
    
    description  = """Just general misc commands"""

    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
    @commands.command(pass_context = True)
    async def hello(self,ctx): # Says hello
        """Says hello. syntax: s.hello"""
        if(await Helper.isBanned(self,ctx) == True): # Checks bans
            return
        
        if(await Helper.isPerms(self,ctx,3)): # Checks permissions
            await self.bot.say("Hello!") # Says hello
            
            await Helper.log(self,str(ctx.message.author),"hello",str(ctx.message.timestamp)) # Logs command

    @commands.command(pass_context = True)
    async def headpat(self,ctx): # Display's a random headpat from folder
        """Returns a random headpat. syntax: s.headpat"""
        if(await Helper.isBanned(self,ctx) == True): # Checks bans
            return
        if(await Helper.isPerms(self,ctx,3)): # Checks permissions
            with open("./memes/Headpats/"+str(random.choice(os.listdir("./memes/Headpats/"))), 'rb') as f: # Opens file in headpat folder
                await self.bot.send_file(ctx.message.channel, f) # Sends headpat

        await Helper.log(self,str(ctx.message.author),"headpat",str(ctx.message.timestamp)) # Logs command

    @commands.command(pass_context = True)
    async def meme(self,ctx): # Display's a random headpat from folder
        if(await Helper.isBanned(self,ctx) == True): # Checks ban
            return
        if(await Helper.isPerms(self,ctx,3)): # Checks permissions 
            with open("./memes/Memes/"+str(random.choice(os.listdir("./memes/Memes/"))), 'rb') as f: # Opens file in meme folder
                await self.bot.send_file(ctx.message.channel, f) # Sends memes
        await Helper.log(self,str(ctx.message.author),"meme",str(ctx.message.timestamp)) # Logs command

    @commands.command(pass_context = True)
    async def quote(self,ctx): # Display's a random quote
        """Gets a random quote. syntax: s.quote"""
        if(await Helper.isBanned(self,ctx) == True): # Checks bans
            return
        if(await Helper.isPerms(self,ctx,3)): # Checks permissions
            r = requests.get(url="http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1&callback=t") # Gets quotesonedesign api
            r = r.json() # Converts it to json
            quoteData = r[0] # Gets all the data in the array
            name = quoteData["title"] # Gets the author of the quote
            quote = quoteData["content"].replace("<p>","") # Removes some of the html junk
            quote = quote.replace("</p>","")
            quote = quote.replace("&#8217;","'")
            #TODO: change to embed
            await self.bot.say('"'+quote+'"'+" - "+name) # Says quote
            await Helper.log(self,str(ctx.message.author),"quote",str(ctx.message.timestamp)) # Logs command



    @commands.command(pass_context = True)
    async def pwnd(self,ctx,user : str): # Display's if account was hacked
        """Returns if the account was hacked. syntax: s.pwnd [email]"""
        if(await Helper.isBanned(self,ctx) == True): # Checks bans
            return
        if(await Helper.isPerms(self,ctx,2)): # Checks permissions
            if(user.find("@") == -1 and user.find(".") == -1 or user == ""): # Validation of input
               await self.bot.say("Invalid address")
               return

            r = requests.get(url="https://haveibeenpwned.com/api/breachedaccount/"+user) # Gets haveibeenpwnd api
            if(r.status_code == 404): # If the user can't be found
                await self.bot.say(":clap: "+user+" has not been hacked :clap:")
                return
                
            try:
                r = r.json()  # Attempt to make a json out of the data              
            except:
                await self.bot.say("API down, try again later!") # If the json can't be created asume that the falsesly returned a blank request
                return
            await self.bot.say(user+" has been in the following exploits:") # If all checks pass display exploited databases
            for info in r:
                await self.bot.say(info)
            await self.bot.say("~~~~END~~~~")
            await Helper.log(self,str(ctx.message.author),"pwnd "+user,str(ctx.message.timestamp)) # Logs command

    @commands.command(pass_context = True)
    async def wiki(self,ctx): # Wiki search
        """Searches wikipedia. syntax: s.wiki [Topic]"""
        await self.bot.say(":thinking:")
        
        message = ctx.message.content.replace("s.wiki ", "") # Gets message
        finished = False
        title = message 
        try: # Word wrapping plus exception handling

            #TODO: make wordwrap function to stop reuse
            wiki = wikipedia.summary(message)
            m = []
            while not finished: # This loop is to bypass the 2000 word limit allowed by discord, I do this by spliting the description into seperate messages
                r = "" # Is the result of the concatination of the words
                for letters in wiki: # This loops through every letter in the sentence
                   r += letters
                   if(len(r) >= 1900): #When the amount of words is greater than 1900 then add a new embed (I chose this number for padding)
                       m.append(discord.Embed(title=title,description=r,colour=0x71368a))
                       r = ""
                m.append(discord.Embed(title=title,description=r+"[CONTINUE]",colour=0x71368a)) # When the loops finished there might be a few letters or words left out the intial loop, this is just here to make sure the everything is displayed
                finished = True
            for x in range(len(m)): # Prints all messages
                await self.bot.say(embed=m[x])

        except wikipedia.exceptions.DisambiguationError as e: # Else print recommendations
                r = "" # Concatination of all letters
                m = [] # The array of texts
                s = str(e) # Converts exception to string
                for letters in s: # for every letter in string
                   r += letters # Add it to r
                   if(len(r) >= 1900): # Add every 1900 words to a new message
                       m.append(discord.Embed(title=title,description=r+"[CONTINUE]",colour=0x71368a))
                       r = ""
                m.append(discord.Embed(title=title,description=r,colour=0x71368a)) # Adds any left over words to another item
                finished = True
                for x in range(len(m)): # Say all recommendations
                    await self.bot.say(embed=m[x])
                    
        except wikipedia.exceptions.PageError: # If nothing at all found
            await self.bot.say("I got nothing on that, sorry.")
        await Helper.log(self,str(ctx.message.author),"wiki "+message,str(ctx.message.timestamp)) # Logs command
    @commands.command(pass_context = True)
    async def say(self,ctx): # Parrots a message
        """Repeats what you say. syntax s.say [stuff]"""
        if(await Helper.isBanned(self,ctx) == True): # Check bans
            return
        if(await Helper.isPerms(self,ctx,3)): #Checks permissions
            msg = ctx.message.content.replace("s.say ","") # Removes prefix
            if(msg == "s.say"):
                await self.bot.say("```tell me what to say ya goose```") # If nothing is inpt
                return
            
            await self.bot.say(msg) # Say's the message
            await Helper.log(self,str(ctx.message.author),"say "+msg,str(ctx.message.timestamp)) # Logs command


    @commands.command(pass_context = True)
    async def mumbo(self,ctx): # Creates a nonsense message from a message a user inputs into it
        if(await Helper.isBanned(self,ctx) == True): # Check bans
            return
        if(await Helper.isPerms(self,ctx,3)): #Checks permissions
            text = ctx.message.content.replace("s.mumbo ", "") # Removes the message itself
            text = nltk.word_tokenize(text) # Uses the NLTK libary to tokenize the sentence 
            text.append(" ") # Adds a space into the array so that random spaces can be applied to the 
            newSentence = "" # Creates a placeholder for the new sentence
            for words in text: # Itterates through the words and randomly selects a new word
                newSentence+= random.choice(text)
                newSentence+= " "
            await self.bot.say(newSentence) # Say the new sentence
            await Helper.log(self,str(ctx.message.author),"mumbo " + newSentence,str(ctx.message.timestamp)) # Logs command
        
            
        
        
    @commands.command(pass_context = True)
    async def gifr(self,ctx): # Display's a random gif from Giphy
        """Returns random gif. syntax: s.gifr"""
        if(await Helper.isBanned(self,ctx) == True): # Checks ban
            return
        if(await Helper.isPerms(self,ctx,3)): # Checks permission

            img = giphypop.random_gif() # Gets random giphy link
            await self.bot.say(img.url) # Show image
            await Helper.log(self,str(ctx.message.author),"gifr",str(ctx.message.timestamp)) # Logs command

    @commands.command(pass_context = True)
    async def gif(self, ctx): # Display's a gif from a selected phrase from giphy
        """Returns gif syntax: s.gif [phrase]"""
        if(await Helper.isBanned(self,ctx) == True): # Checks bans
            return
        
        if(await Helper.isPerms(self,ctx,3)): # Checks permissions
            phrase = ctx.message.content.replace("s.gif","") # Gets the term
            if(ctx.message.content == "s.gif"): # If the search term was blank then return friendly message
                await self.bot.say("```Type search ya dingus```")
            img = giphypop.translate(phrase) # If validation is ok search the phrase
            if(img is None): # If no image is found alert the user
                await self.bot.say("I couldn't find it try looking something else up.")
            await self.bot.say(img.url) #Display image
            await Helper.log(self,str(ctx.message.author),"giphy "+phrase,str(ctx.message.timestamp)) # Logs command



    @commands.command(pass_context = True)    
    async def ping(self,ctx): # Says pong
        """Returns pong. syntax: s.ping"""
         
        if(await Helper.isBanned(self,ctx) == True): # Checks bans
            return
        if(await Helper.isPerms(self,ctx,3)): # Checks permissions
            await self.bot.say("Pong!") # Say pong
            await Helper.log(self,str(ctx.message.author),"ping",str(ctx.message.timestamp)) # Logs command

    @commands.command(pass_context = True)    
    async def pong(self,ctx): # Says ping
        """Returns ping. syntax s.pong"""
        if(await Helper.isBanned(self,ctx) == True): # Checks bans
            return
        if(await Helper.isPerms(self,ctx,3)): # Checks permissions
            await self.bot.say("Ping!") # Says ping
            await Helper.log(self,str(ctx.message.author),"pong" ,str(ctx.message.timestamp)) # Logs command

    @commands.command(pass_context = True)    
    async def magic8(self,ctx): # Magic 8ball
        """8ball. syntax s.magic8"""
        if(await Helper.isBanned(self,ctx) == True): # Checks bans
            return
        if(await Helper.isPerms(self,ctx,3)): # Checks permissions
            # Array of responses
            phrase = ["It is certain","Without a doubt","Yes definitely","You may rely on it","As I see it, yes","Most likely","Outlook good","Yes","Signs point to yes","Reply hazy try again","Ask again later","Better not tell you now","Cannot predict now","Concentrate and ask again","Don't count on it","My reply is no","My sources say no","Outlook not so good"," Very doubtful"]
            await self.bot.say(str(random.choice(phrase))) # Say response
            await Helper.log(self,str(ctx.message.author),"8ball",str(ctx.message.timestamp)) # Logs command





def setup(bot):
    bot.add_cog(General(bot))









