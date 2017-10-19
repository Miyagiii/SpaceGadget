#
#   Currently in development, buggy as hell and not commented yet, i do not recommend using this module
#
#



import discord,youtube_dl,time,asyncio
from discord.ext import commands
from plugins.Helper import Helper

class Music:
    description = """Music"""
    
    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.player = None
        self.isPlaying = False
        self.queue = []
        self.sVotes = []
        
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context = True)
    async def q(self,ctx):
        if(await Helper.isBanned(self,ctx)):
            return
        if(await Helper.isPerms(self,ctx,3)):
            if(ctx.message.content == "" or ctx.message.content == " " or ctx.message.content =="s.q"):     
                await self.bot.say("You actually need to search for something ya dingus")
                return
            await self.bot.say(embed=discord.Embed(title="Added: "+ctx.message.content.replace("s.q ","")+" to queue",description="",colour = 0x206694)) # Display's the synopsis with all relivent data in the embed
            self.queue.append(ctx.message.content.replace("s.q ",""))
            if(len(self.queue) == 1):
                await self.play(ctx)
    @commands.command(pass_context = True)
    async def skip(self,ctx):
        if(len(self.queue) == 0):
            await self.bot.say("No songs in queue  ¯\_(ツ)_/¯")
        if(await Helper.isPerms(self,ctx,1)):
            await self.bot.say("`Skip sucessful`")
            self.sVotes = []
            del self.queue[0]
            self.player.stop()
            if(len(self.queue) >0):
                await self.bot.say("`Skipping to "+self.queue[0]+"`")
                await self.play(ctx)
            else:
                return
        if(await Helper.isBanned(self,ctx)):
            
            return
        if(await Helper.isPerms(self,ctx,3)):
            if(self.isPlaying == False):
                await self.bot.say("Bot isn't playing anything")
                return
            if(self.voice == None):
                await self.bot.say("Bot not in voice chat")
                return
            for items in self.sVotes:
                if(ctx.message.author.id == items):
                    await self.bot.say("Can't vote again")
                    return
            self.sVotes.append(ctx.message.author.id)
            await self.bot.say("`Skip - "+str(len(self.sVotes))+"/"+str(int(len(self.voice.channel.voice_members) /2))+"`")
            if(len(self.sVotes) >= (len(self.voice.channel.voice_members) /2)):
                await self.bot.say("`Skip sucessful`")
                self.sVotes = []
                del self.queue[0]
                self.player.stop()
                if(len(self.queue) >0):
                    await self.bot.say("`Skipping to "+self.queue[0]+"`")
                    await self.play(ctx)
                else:
                    return
            
        
    @commands.command(pass_context = True)
    async def show_queue(self,ctx):
        r = ""
        x = 0
        if(len(self.queue) == 0):
            await self.bot.say(embed=discord.Embed(title="Nothing in queue!",description="",colour = 0x206694)) # Display's the synopsis with all relivent data in the embed
            return
            
        for items in self.queue:
            x+=1
            r+="`#"+str(x)+":` "+items+" - "+ctx.message.author.name+"\n"
        await self.bot.say(embed=discord.Embed(title="Queue",description=r,colour = 0x206694)) # Display's the synopsis with all relivent data in the embed

               
    @commands.command(pass_context = True)
    async def join_vc(self,ctx): 
        """Joins a voice chat. Syntax: s.join_vc"""
        if(await Helper.isBanned(self,ctx)):
            return
        if(await Helper.isPerms(self,ctx,3)):
            if(self.isPlaying == True):
                await self.bot.say("Can't move chat while playing music")
                return
            if(self.bot.voice_client_in(ctx.message.author.server) is not None):
                self.voice = self.bot.voice_client_in(ctx.message.author.server)
            channel = ctx.message.author.voice.voice_channel
            if( ctx.message.author.voice.voice_channel != self.voice and self.voice is not None):
                self.voice = await self.voice.disconnect()
            if(ctx.message.author.voice.voice_channel is None):
                await self.bot.say("```You have to be in a chat for the bot to join you, MORON!!!```")
                return
            if(self.voice is not None):
                self.voice = await self.voice.move_to(channel)
                return
            self.voice = await self.bot.join_voice_channel(channel)
            await Helper.log(self,str(ctx.message.author),"joined vc "+channel.name,str(ctx.message.timestamp))

    async def clears(self,ctx):
        for x in range(0,len(self.queue)):
            del self.queue[x]
            self.isPlaying = False
    @commands.command(pass_context = True)
    async def clear(self,ctx):
        if(await Helper.isBanned(self,ctx)):
           return
        if(await Helper.isPerms(self,ctx,1)):
            if(self.player is not None):
                self.player.stop()
            await self.clears(ctx)
        
        

    @commands.command(pass_context = True)
    async def disconnect_vc(self,ctx):
        """Disconnects bot from voice chat. Syntax: s.disconnect_vc"""
        if(await Helper.isBanned(self,ctx)):
           return
        if(await Helper.isPerms(self,ctx,3)):
            if(self.isPlaying == True):
                if(await Helper.isPerms(self,ctx,1)):
                    await self.bot.say("Administrative disconnect Successful")
                    await self.clears(ctx)
                else:
                    await self.bot.say("You cannot disconnect bot while it's playing music")
                    return

            if(self.bot.voice_client_in(ctx.message.author.server) is not None):
                 self.voice = self.bot.voice_client_in(ctx.message.author.server) 
                 await self.voice.disconnect()
                 self.isPlaying = False
            else:
                await self.bot.say("Bot not in voice chat")
                return
            await Helper.log(self,str(ctx.message.author),"disconnected from vc",str(ctx.message.timestamp))

    async def play(self,ctx):
        """Play music. Syntax: s.play [url]"""
        while(len(self.queue) != 0):
            if(len(self.queue) == 0):
                return
            if(self.isPlaying == True):
                self.player.stop()
            if(self.voice is None and self.bot.voice_client_in(ctx.message.author.server) is not None):
                self.voice = self.bot.voice_client_in(ctx.message.author.server)
            elif(ctx.message.author.voice_channel is not None and self.voice is None):
                self.voice = await self.bot.join_voice_channel(ctx.message.author.voice_channel)
            else:
                self.voice = self.bot.voice_client_in(ctx.message.author.server)
            if(self.voice is None):
                if(ctx.message.author.voice.voice_channel is not None ):
                    self.voice = await self.bot.join_voice_channel(ctx.message.author.voice.voice_channel)
                else:                   
                    await self.bot.say("Bot isn't in a voice channel")
                    return
            message = self.queue[0]#ctx.message.content.replace("s.play ","")
            await self.bot.say(embed=discord.Embed(title="Now Playing: "+message,description="",colour = 0x206694)) # Display's the synopsis with all relivent data in the embed
            beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
            ytdl_meta_opts = {
                    'default_search': 'auto',
                    'simulate': True,
                    'quiet': True,
            }
            self.player = await self.voice.create_ytdl_player(message,ytdl_options=ytdl_meta_opts,before_options=beforeArgs)
                
            self.player.volume = 1
            self.player.start()
            self.isPlaying = True
            await Helper.log(self,str(ctx.message.author),"played "+message,str(ctx.message.timestamp))
            await asyncio.sleep(self.player.duration+5)
            if(self.isPlaying == False):
                return
            del self.queue[0]
            self.player.stop()

        await self.bot.say("No songs in queue  ¯\_(ツ)_/¯")
        self.bot.isPlaying = False
            
    @commands.command(pass_context = True)
    async def stop(self,ctx):
        """Stops music. Syntax: s.stop"""
        if(await Helper.isBanned(self,ctx)):
            return
        if(await Helper.isPerms(self,ctx,1)):
            if(self.player is None):
                await self.bot.say("No song playing!")
            self.player.stop()
            self.isPlaying = False
            await self.clears(ctx)
            await Helper.log(self,str(ctx.message.author),"Stop",str(ctx.message.timestamp))

            
def setup(bot):
    bot.add_cog(Music(bot))
