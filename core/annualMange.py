import aiosqlite

class AnnualManage:

    def __init__(self, dbPath: str) -> None:
        self.db: aiosqlite.Connection
        self.dbPath: str = dbPath
    
    async def __ainit__(self) -> None:
        self.db = await aiosqlite.connect(self.dbPath)
        await self.db.execute(
            '''
            CREATE TABLE IF NOT EXISTS members  (
            id INTEGER PRIMARY KEY,
            annual INTEGER NOT NULL
            );
            '''
        )
        await self.db.commit()
    
    async def disconnect(self) -> None:
        await self.db.close()
    
    async def testServer(self, **args) -> str:
        print(self.db)
        return "qq"
    
    async def insertUser(self, userId: int, **args) -> None:
        checking = await self.checkUser(userId)
        if (checking is True):
            return
        query = '''
                INSERT INTO members(
                id,
                annual
                )
                VALUES(?, ?)
                '''
        cursor = await self.db.execute(query, (userId, 25))
        await cursor.close()
        await self.db.commit()
        print(query)

        
        
    
