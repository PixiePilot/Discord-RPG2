import pyodbc
language = {}

def strings(cursor,id,language = 'EN'):
    return cursor.execute(f'SELECT content FROM StringResource_{language} WHERE ID = {id}').fetchval()
    
