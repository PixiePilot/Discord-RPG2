from ast import Str, Subscript, match_case
from types import NoneType
import pyodbc
from http import client
import discord
from discord.ext import commands
connection = string_connection = ('Driver={SQL Server};'
                    'Server=localhost;'
                    'DataBase=ProjectRPG;'
                    'Trusted_Connection=yes;')





class Database():

    conn = None
    def __init__(self) -> None:
        self.conn = pyodbc.connect(connection)
        self.cursor = self.conn.cursor()
        pass
    def request_weapon_stats(self,id):
        return self.cursor.execute(f'SELECT * from ItemResource WHERE item_id = {id}').fetchone()

        return
    def stats_request(self,char_id):
        return self.cursor.execute(f"SELECT * FROM characters WHERE char_id = {char_id}").fetchall()


    def string_resource(self,id,language = 'EN'):
        return self.cursor.execute(f'SELECT content FROM StringResource_{language} WHERE ID = {id}').fetchval()

    async def authencation(self,ctx):
        cursor = self.cursor
        cursor.execute(f'SELECT ID FROM Accounts WHERE DiscordID = {ctx.author.id}')
        check = cursor.fetchall()
        if len(check) >= 1:
            await ctx.send(self.string_resource(1))
            return True
        try:
            cursor.execute(f'''INSERT INTO [dbo].[Accounts] ([ID], [DiscordID], [CreationDate]) 
            VALUES ((SELECT MAX(ID) +1 FROM Accounts), {ctx.author.id}, GETDATE());''').commit()

            print(f'{ctx.author.id} has successfully Registered an account')
            await ctx.send(f'{ctx.author} {self.string_resource(2)}')
            return False
        except:
            print(f'{ctx.author} has tried to register but failed')
            await ctx.send(self.string_resource(3))
        pass

    async def char_count(self,id,check=False):
        cursor = self.cursor
        user_id = cursor.execute(f'SELECT ID FROM Accounts WHERE DiscordID = {id}').fetchval()
        char_list = cursor.execute(f'SELECT id FROM characters WHERE char_id = {user_id} ').fetchall()
        if len(char_list) >= 8 and check:
            return True
        return char_list
    
    def create_char(self,name,job_query):
        self.cursor.execute(f"INSERT INTO [dbo].[characters] ([char_id], [name], [creation_date], [block], [vit], [agi], [str], [wis], [dex], [int], [class], [wear_1], [wear_2], [id], [current_hp], [max_hp]) VALUES ((SELECT MAX(char_id) +1 from characters), '{name}', GETDATE(), 0, 1, 1, 1, 1, 1, 1, {job_query}, 0, 0, (SELECT MAX(id) +1 from characters), 10, 10);").commit()
        pass



class Struct_player():
    char_id = None
    max_hp = None
    max_mp = None
    cur_hp = None
    cur_mp = None
    armor = None
    vit = None
    str = None
    agi = None
    dex = None
    wis = None
    int = None
    job = None
    wear1 = None
    wear2 = None
    exp = None
    level = None
    # -----None raw stats------
    armor = 0
    accuracy = 0
    magical_accuracy = 0
    physical_atk = 0
    magical_atk = 0
    database = Database()
    def __init__(self,char_id) -> None:
        raw_stat = self.database.stats_request(char_id)
        
        self.char_id = char_id
        self.job =      raw_stat[0][10]
        self.vit =      raw_stat[0][4] # vit = 2 armor 3 hp
        self.agi =      raw_stat[0][5] # 3 evasion 1 ranged damage
        self.str =      raw_stat[0][6] # 3 melee damage
        self.wis =      raw_stat[0][7] # magical accuracy 3 magical defense 1
        self.dex =      raw_stat[0][8] # physical accuracy 2 ranged damage 3
        self.int =      raw_stat[0][9] # magic point 1 magic damage 3
        self.max_hp =   raw_stat[0][15] # max hp raw
        self.cur_hp =   raw_stat[0][14] # curr hp raw
        self.max_mp =   raw_stat[0][15] # max hp raw
        self.cur_mp =   raw_stat[0][16] # cur mp raw
        self.exp =      raw_stat[0][18] # XP
        self.level =    raw_stat[0][19] # Level
        self.wear1 =    raw_stat[0][11] # first equippable slot ( weapon )
        self.wear2 =    raw_stat[0][12] # second equippable slot ( armor )
        
    def weapon_struct(self):
        weapon_info = (self.database.request_weapon_stats(self.wear1))
        try:
            self.wear_type =   weapon_info[1]
            self.weapon_patk = weapon_info[9]
            self.weapon_matk = weapon_info[10]
            self.weapon_str  = weapon_info[2]
            self.weapon_agi  = weapon_info[3]
            self.weapon_dex  = weapon_info[4]
            self.weapon_wis  = weapon_info[5]
            self.weapon_int  = weapon_info[6]
            self.weapon_vit  = weapon_info[7]
        except TypeError:
            print(f'missing item id on character: {self.char_id} item id: {self.wear2} (wear1)')
        match self.wear_type:

            case 1: #type 1 == Melee
                if self.job == 1: # Gains armor based on STR.
                    self.accuracy = self.level*2
                    self.weapon_patk = self.weapon_patk + (self.level * 3) 
                self.physical_atk = (self.physical_atk + (self.str + self.weapon_str) * 3) + self.weapon_patk
                self.accuracy = self.accuracy + (self.dex * 2) + self.weapon_dex
                print(f'p.atk:{self.physical_atk} acc:{self.accuracy}')
                return
            
            case 2: # type 2 == Ranged
                if self.job == 2:
                    self.accuracy = self.level*3
                    self.weapon_patk = self.weapon_patk + (self.level * 3) 
                self.physical_atk = (self.physical_atk + (self.dex + self.weapon_dex) * 2) + self.weapon_patk + (self.agi + self.weapon_agi)
                self.accuracy = self.accuracy + (self.dex * 2) + self.weapon_dex
                print(f'p.atk:{self.physical_atk} acc:{self.accuracy}')
                return

            case 3: # type 3 == magical
                if self.job == 3:
                    self.magical_accuracy = self.level*2
                    self.weapon_patk = self.weapon_patk + (self.level * 3) 
                self.magical_atk = (self.magical_accuracy + (self.int + self.weapon_int) * 3) + self.weapon_matk
                self.magical_accuracy = self.magical_accuracy + (self.wis * 2) + self.weapon_wis
                print(f'p.atk:{self.magical_atk} acc:{self.magical_accuracy}')
                return
        print(f'Something went wrong with the weapon type on user :{self.char_id}')
        return
    def armor_struct(self):
        job_check = lambda job: job == 1
        print(job_check(self.job))
        armor_info = (self.database.request_weapon_stats(self.wear2))
        try:
            self.armor_agi  = armor_info[3]
            self.armor_dex  = armor_info[4]
            self.armor_wis  = armor_info[5]
            self.armor_int  = armor_info[6]
            self.armor_vit  = armor_info[7]
            self.armor      = armor_info[8]
            
        except TypeError:
            print(f'missing item id on character: {self.char_id} item id: {self.wear2} (wear2)')
        self.armor = self.armor + self.weapon_vit + self.armor_vit + (self.vit * 2) + (self.str * job_check(self.job))
        print(f'armor:{self.armor}')
            
        pass
    def stat_calc(self):
        self.weapon_struct()
        self.armor_struct()
        pass
    def attributes_str(self) -> Str:
        attributes = f'ID:{self.char_id} max_hp:{self.max_hp} max_mp:{self.max_mp} armor:{self.armor} vit:{self.vit} str:{self.str} agi:{self.agi} dex:{self.dex} wis:{self.wis} int:{self.int} max_hp:{self.max_hp} cur_hp{self.cur_hp} max_mp:{self.max_mp} cur_mp:{self.cur_mp} level:{self.level} experience:{self.exp} Equip1:{self.wear1} Equip2:{self.wear2} job:{self.job} p.atk:{self.magical_atk} acc:{self.magical_accuracy} m.atk:{self.physical_atk} acc:{self.accuracy}'
        return attributes


print('Database module: ok')