import aiosqlite
from .model.memberModel import MemberModel

ANNUAL_START_COUNT = 25

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
            reason VARCHAR(255) NOT NULL,
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
        '''
        유저가 생성하는 함수입니다.
        '''
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
        '''
        유저가 존재하는지 확인하는 함수입니다.
        '''
        query = '''
                SELECT * FROM members WHERE id=?
                '''
        cursor = await self.db.execute(query, (userId, ))
        record = await cursor.fetchone()
        await cursor.close()
        return record != None
    
    
    async def makeUser(self, userId: int):
        '''
        유저가 존재하는지 확인하고 없다면 유저를 생성하는 함수입니다.
        '''
        if (await self.checkUser(userId) is False):
            await self.insertUser(userId)
    
    async def getUser(self, userId: int, **args) -> MemberModel:
        '''
        유저에 대한 정보를 얻어오는 함수입니다.
        '''
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
        '''
        유저의 연차 개수를 얻어오는 함수입니다.
        '''
        if (await self.checkUser(userId) is False):
            await self.insertUser(userId)
        query = '''
                SELECT * FROM annuals WHERE user_id=?
                '''
        cursor = await self.db.execute(query, (userId, ))
        record = await cursor.fetchall()
        await cursor.close()
        sum = 0
        for i in record:
            sum += i[1]


        return ANNUAL_START_COUNT-len(sum)

        


        
        
    
