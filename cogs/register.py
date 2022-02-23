
from http import client
import discord
from discord.ext import commands
import pyodbc
from functions import stringfunctions
from structs import Structs
connection = string_tele = ('Driver={SQL Server};'
                    'Server=localhost;'
                    'DataBase=ProjectRPG;'
                    'Trusted_Connection=yes;')
class commands(commands.Cog):

    def __init__(self,bot):

        self.bot = client


        self.status = 'ok'
        try:
            self.conn = Structs.Database()
        except:
            self.status = 'Failed'
        print(f'Register module : {self.status}')

    @commands.command()
    async def register(self,ctx):
        account = await self.conn.authencation(ctx)
        char_list = await self.conn.char_count(ctx.author.id)
        print(char_list)
        if len(char_list) == 0:
            await ctx.send(self.conn.string_resource(5))
        pass

    @commands.command()
    async def create(self,ctx,name,job):
        checker = await self.conn.char_count(ctx.author.id,True)
        print(checker)
        if checker == True:
            await ctx.send(self.conn.string_resource(4))
            return
        if job == 'warrior':
            job_query = 1
        elif job == 'hunter':
            job_query = 2
        elif job == 'mage':
            job_query = 3 
        else:
            return
        self.conn.create_char(name,job_query)
        pass

    @commands.command()
    async def test(self,ctx):
        test = Structs.Struct_player(2)
        test.stat_calc()
        print(test.attributes_str())
        pass
def setup(bot):
         bot.add_cog(commands(bot))