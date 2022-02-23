import pyodbc
from functions import stringfunctions


async def authencation(ctx,cursor):
    cursor.execute(f'SELECT ID FROM Accounts WHERE DiscordID = {ctx.author.id}')
    check = cursor.fetchall()
    if len(check) >= 1:
        await ctx.send(stringfunctions.strings(cursor,1))
        return True
    try:
        cursor.execute(f'''INSERT INTO [dbo].[Accounts] ([ID], [DiscordID], [CreationDate]) 
        VALUES ((SELECT MAX(ID) +1 FROM Accounts), {ctx.author.id}, GETDATE());''').commit()

        print(f'{ctx.author.id} has successfully Registered an account')
        await ctx.send(f'{ctx.author} {stringfunctions.strings(cursor,2)}')
        return False
    except:
        print(f'{ctx.author} has tried to register but failed')
        await ctx.send(stringfunctions.strings(cursor,3))


async def char_count(ctx,cursor,check=False):
    user_id = cursor.execute(f'SELECT ID FROM Accounts WHERE DiscordID = {ctx.author.id}').fetchval()
    char_list = cursor.execute(f'SELECT id FROM characters WHERE char_id = {user_id} ').fetchall()
    if len(char_list) < 8 and check:
        return True
    return char_list


async def char_creation(ctx,cursor):
    await ctx.send('You have not created a character yet, Would you like to create one?')
    return