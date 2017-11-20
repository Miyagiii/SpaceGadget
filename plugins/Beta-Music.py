#
#   Currently in development, buggy as hell and not commented yet, i do not recommend using this module
#
#
import discord,youtube_dl,time,asyncio,datetime,locale
from discord.ext import commands
from plugins.Helper import Helper

class Player:

    def __init__(self, bot):
        self.bot = bot
        self.player = None
        self.skipVotes = [] 
        if(len(list(self.bot.voice_clients)) <= 0):
            self.voice = None
        else:
            self.voice = list(self.bot.voice_clients)[0]
        self.queue = []

    @commands.command(pass_context = True)
    async def joinvc(self,ctx):
        if(await Helper.isBanned(self,ctx)):
            return
        if(await Helper.isPerms(self,ctx,3)):
            if(ctx.message.author.voice.voice_channel is None):
                await self.bot.say("You must join a voice channel first to add the bot.")
                return
            if(self.player is not None):     
                if(self.player.is_playing()):
                    await self.bot.say("Cannot move bot while is playing.")
                    return
            if(self.bot.is_voice_connected(ctx.message.author.server) == False):
                self.voice = await self.bot.join_voice_channel(ctx.message.author.voice.voice_channel)
            else:
                self.voice = list(self.bot.voice_clients)[0]
                self.voice = await self.voice.move_to(ctx.message.author.voice.voice_channel)
                
    @commands.command(pass_context = True)
    async def disconnectvc(self,ctx):
        if(await Helper.isBanned(self,ctx)):
            return
        if(await Helper.isPerms(self,ctx,3)):
            if(self.bot.is_voice_connected(ctx.message.author.server) == False):                  
                await self.bot.say("Bot not in a voice channel")
                return
        if(self.player is not None):     
                if(self.player.is_playing()):
                    await self.bot.say("Cannot move bot while is playing.")
                    return

        if(self.bot.is_voice_connected(ctx.message.author.server) and self.voice == None):
            self.voice = list(self.bot.voice_clients)[0]
        await self.voice.disconnect()
    @commands.command(pass_context = True)
    async def p(self,ctx):
        if(await Helper.isBanned(self,ctx)):
            return
        if(await Helper.isPerms(self,ctx,3)):
            if(len(self.queue) >= 25):
                await self.bot.say(embed=discord.Embed(title="Notice:",description="Cannot add more than 25 tracks at a time",colour = 0x206694))
                return
            url = ctx.message.content.replace(self.bot.config['prefix']+"p ", "")
            if(self.voice == None and ctx.message.author.voice.voice_channel is not None):
                if(self.bot.is_voice_connected(ctx.message.author.server) == False):
                    self.voice = await self.bot.join_voice_channel(ctx.message.author.voice.voice_channel)
                else:
                    self.voice = list(self.bot.voice_clients)[0]
                    self.voice = await self.voice.move_to(ctx.message.author.voice.voice_channel)

            if(self.voice == None):
                await self.bot.say("Not in voice channel")
                return
            if(url == ""):
                await self.bot.say("You need to search something")
                return
            
            await self.retrieveSong(url,ctx.message.author,ctx)
    @commands.command(pass_context = True)
    async def q(self,ctx):
        if(await Helper.isBanned(self,ctx)):
            return
        if(await Helper.isPerms(self,ctx,3)):
            if(len(self.queue) <= 0):
                await self.bot.say(embed=discord.Embed(title="Notice:",description="No tracks in queue",colour = 0x206694))
                return
            embed = discord.Embed(title="Queue:",colour = 0x206694)
            for x in range(0,len(self.queue)):
                embed.add_field(name="---------------------------------------------------------------------------------------------------",
                                value="**"+self.queue[x].name+"** : `"+str(self.queue[x].duration)+"` - **"+self.queue[x].requester.name+"**")
            await self.bot.say(embed=embed)
            

            
    async def retrieveSong(self,url,requester,ctx):
        if(len(self.voice.channel.voice_members) > -3):
            if(len(self.queue) >= 3):
                if(self.queue[-1].requester == requester and self.queue[-2].requester == requester and self.queue[-3].requester == requester):
                    await self.bot.say("You chose the last three songs, give someone else a go")
        ytdl_meta_opts = { 
                        'default_search': 'auto',
                        'simulate': True,
                        'quiet': True,
                }
        try:
            songRet = await self.voice.create_ytdl_player(url,ytdl_options=ytdl_meta_opts)
        except Exception as e:
            await self.bot.say(embed=discord.Embed(title="Notice:",colour = 0x206694,description="Something went wrong :/ "+str(e)))
            return
            
        locale.setlocale(locale.LC_ALL, "en-GB")
        self.queue.append(Song(songRet.title,datetime.timedelta(seconds=songRet.duration),songRet.uploader,locale.format("%d",songRet.views,grouping=True),locale.format("%d",songRet.dislikes,grouping=True),locale.format("%d",songRet.likes,grouping=True),songRet.upload_date,songRet.download_url,requester))
        
        embed = discord.Embed(title="Adding: "+self.queue[-1].name,colour = 0x206694,url=self.queue[-1].url)
        embed.add_field(name="Duration:", value=self.queue[-1].duration)
        embed.add_field(name="Uploader:", value=self.queue[-1].uploader)
        embed.add_field(name="Views:", value=self.queue[-1].views)
        embed.add_field(name="Likes:", value=self.queue[-1].likes)
        embed.add_field(name="Dislikes:", value=self.queue[-1].dislikes)
        embed.add_field(name="Upload Date:", value=self.queue[-1].uploadDate)
        embed.set_author(name=self.queue[-1].requester.name, icon_url=requester.avatar_url)
        await self.bot.say(embed=embed)
        songRet.start()
        songRet.stop()
        if(len(self.queue) <= 1):
            await self.play(ctx)
    async def play(self,ctx):
        while len(self.queue) != 0:
            try:
                song = self.queue[0]
                beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                ytdl_meta_opts = { 
                        'default_search': 'auto',
                        'simulate': True,
                        'quiet': True,
                }
                self.player = await self.voice.create_ytdl_player(song.url,ytdl_options=ytdl_meta_opts,before_options=beforeArgs)
                self.player.start()
                embed = discord.Embed(title="Now playing: "+song.name,colour = 0x206694,url=song.url)
                embed.add_field(name="Duration:", value=song.duration)
                embed.add_field(name="Uploader:", value=song.uploader)
                embed.add_field(name="Views:", value=song.views)
                embed.add_field(name="Likes:", value=song.likes)
                embed.add_field(name="Dislikes:", value=song.dislikes)
                embed.add_field(name="Upload Date:", value=song.uploadDate)
                embed.set_author(name=song.name, icon_url=song.requester.avatar_url)
                await self.bot.say(embed=embed)
                while self.player.is_playing():
                    await asyncio.sleep(0.03)
                self.player.stop()
                del self.queue[0]
            except Exception as e:
                await self.bot.say(embed=discord.Embed(title="Notice:",colour = 0x206694,description="Something went wrong :/ "+str(e)))
        self.player.stop()
        
        await self.bot.say(embed=discord.Embed(title="Notice:",colour = 0x206694,description="queue empty¯\_(ツ)_/¯"))

    @commands.command(pass_context = True)
    async def stop(self,ctx):
        if(await Helper.isBanned(self,ctx)):
            return
        if(await Helper.isPerms(self,ctx,1)):
            if(self.player is None or self.player.is_playing() == False):
                await self.bot.say(embed=discord.Embed(title="Notice:",colour = 0x206694,description="Nothing is playing"))

                return
            self.player.stop()
    @commands.command(pass_context = True)
    async def skip(self,ctx): 
        if(await Helper.isBanned(self,ctx)):
            return
        if(await Helper.isPerms(self,ctx,3)):
            if(self.player is None or self.voice is None):
                await self.bot.say(embed=discord.Embed(title="Notice:",colour = 0x206694,description=":no_entry_sign: **Nothing is playing** :no_entry_sign: "))
                return
            if(self.player.is_playing() == False):
                await self.bot.say(embed=discord.Embed(title="Notice:",colour = 0x206694,description=":no_entry_sign: **Nothing is playing** :no_entry_sign: "))
            if(await Helper.getRole(self,ctx,ctx.message.author.id) <= 1):
                await self.doSkip()
                return
            if(len(self.skipVotes) >= 0):
                for ids in self.skipVotes:
                    if(ids == ctx.message.author.id):
                        await self.bot.say("Can't vote twice")
        
                        return
            self.skipVotes.append(ctx.message.author.id)
            await self.bot.say(" Votes required to skip: `"+str(len(self.skipVotes))+"/"+str(int(len(self.voice.channel.voice_members) /2))+"`")
            if(len(self.skipVotes) >= (len(self.voice.channel.voice_members) /2)):
                await self.doSkip()
                await self.bot.say(embed=discord.Embed(title="Notice:",colour = 0x206694,description=":fast_forward: **Skipping** :fast_forward: "))
                self.skipVotes = []
            
                
                
    async def doSkip(self):
        self.player.stop()
        
            
class Song:
    def __init__(self,title,duration,uploader,views,dislikes,likes,uploadDate,url,requester):
        self.name = title
        self.duration = duration
        self.uploader = uploader
        self.views = views
        self.dislikes = dislikes
        self.likes = likes
        self.uploadDate = uploadDate
        self.url = url
        self.requester = requester
def setup(bot):
    bot.add_cog(Player(bot))
