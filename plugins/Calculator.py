# Coded by TheSpaceCowboy
# Git: https://www.github.com/thespacecowboy42534
# Date: ‎19/8/17

#Import
import discord
from discord.ext import commands
from plugins.Helper import Helper

class Calculator:
    description = """Maths stuff"""
    
    def __init__(self, bot): # Class intialisation
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))


    @commands.command(pass_context = True)
    async def add(self,ctx,number1 : float, number2 : float): # Adds two numbers together
        """Adds two numbers. Syntax: s.add [number1] [number2]"""
        
        if(await Helper.isBanned(self,ctx)): # Checks bans
            return
        
        if(await Helper.isPerms(self,ctx,3)): # Checks permissions
            await self.bot.say("The sum of "+str(number1)+" + "+str(number2)+" is "+str(number1+number2))# Displays sum of addition
                               
            await Helper.log(self,str(ctx.message.author),"add",str(ctx.message.timestamp)) # Logs command

    @commands.command(pass_context = True)
    async def minus(self,ctx,number1 : float, number2 : float): # Subtracts two numbers from each other
        """Takesaway two numbers. Syntax: s.minus [number1] [number2]"""
                                    
        if(await Helper.isBanned(self,ctx)): # Checks commands
            return
                               
        if(await Helper.isPerms(self,ctx,3)):  # Checks permissions          
            await self.bot.say("The sum of "+str(number1)+" - "+str(number2)+" is "+str(number1-number2)) # Displays sum of subtraction
                               
            await Helper.log(str(ctx.message.author),"minus",str(ctx.message.timestamp)) # Logs command


    @commands.command(pass_context = True)
    async def times(self,ctx,number1 : float, number2 : float): # Times two numbers together
        """Times two numbers. Syntax: s.times [number1] [number2]"""
                               
        if(await Helper.isBanned(self,ctx)): # Checks bans
            return
                               
        if(await Helper.isPerms(self,ctx,3)): # Checks permsissions

            await self.bot.say("The sum of "+str(number1)+" x "+str(number2)+" is "+str(number1*number2)) # Displays sum of times
                               
            await Helper.log(str(ctx.message.author),"times",str(ctx.message.timestamp))  # Logs command


    @commands.command(pass_context = True)    
    async def divide(self,ctx,number1 : float, number2 : float): # Divde two numbers by each other
        """Divide two numbers. Syntax: s.divide [number1] [number2]"""
                               
        if(await Helper.isBanned(self,ctx)): # Checks bans
            return
                               
        if(await Helper.isPerms(self,ctx,3)): # Checks permissions
                               
            if(number2 == 0): # Error handling if attempting to divide by 0
                
                await self.bot.say("```Cannot divide by zero ya dingus```")
                return
                               
            await self.bot.say("The sum of "+str(number1)+" ÷ "+str(number2)+" is "+str(number1/number2)) # Displays sum of divide
                               
            await Helper.log(str(ctx.message.author),"add",str(ctx.message.timestamp))  # Logs command

def setup(bot):
    bot.add_cog(Calculator(bot)) # Adds cog to bot
