import datetime

def getStringToDateTime(text: str) -> datetime.datetime:
    '''
    2024-03-23 21:18:29.025631 형식의 문자열을 datetime 객체로 반환합니다.
    '''
    return datetime.datetime.strptime(text, "%Y-%m-%d %H:%M:%S.%f")