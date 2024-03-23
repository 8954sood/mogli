import aiosqlite
from .model.memberModel import MemberModel

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
            name VARCHAR(255)
            );
            '''
        )
        await self.db.execute(
            '''
            CREATE TABLE IF NOT EXISTS annuals  (
            id INTEGER PRIMARY KEY,
            annual INTEGER NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id)
                REFERENCES members (user_id) 
            );
            '''
        )
        await self.db.commit()
    
    async def disconnect(self) -> None:
        await self.db.close()
    
    async def testServer(self, **args) -> str:
        print(self.db)
        return "qq"
    
    async def insertUser(self, userId: int, name: str = None, **args) -> None:
        checking = await self.checkUser(userId)
        if (checking is True):
            return
        query = '''
                INSERT INTO members(
                id,
                name
                )
                VALUES(?, ?)
                '''
        cursor = await self.db.execute(query, (userId, name))
        await cursor.close()
        await self.db.commit()
        print(query)

    async def checkUser(self, userId: int, **args) -> bool:
        query = '''
                SELECT * FROM members WHERE id=?
                '''
        cursor = await self.db.execute(query, (userId, ))
        record = await cursor.fetchone()
        await cursor.close()
        return record != None
    
    async def getUser(self, userId: int, **args) -> MemberModel:
        if (await self.checkUser(userId) is False):
            await self.insertUser(userId)
        query = '''
                SELECT * FROM members WHERE id=?
                '''
        cursor = await self.db.execute(query, (userId, ))
        record = await cursor.fetchone()
        await cursor.close()
        
        return MemberModel(record[0], record[1])
    
    async def getUserAnnual(self, userId: int, **args) -> int:
        if (await self.checkUser(userId) is False):
            await self.insertUser(userId)
        query = '''
                SELECT * FROM annuals WHERE user_id=?
                '''
        cursor = await self.db.execute(query, (userId, ))
        record = await cursor.fetchall()
        await cursor.close()
        
        return 25-len(record)
    

        
        
    
