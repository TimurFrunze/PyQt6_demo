import sqlite3
import threading
import os
from sqlite3 import connect
from datetime import datetime, date, timedelta
'''
客户端进行本地存储：创建sqlite3连接池
本地数据库(sqlite3): .exe存放在"output"目录，.db存放在"Database"
        中，每一个数据库存放一类笔记，default.db存放默认类型的笔记
        一张表代表一个类型的笔记，一条记录代表一份笔记
'''


def get_time_str() -> str:
    return datetime.now().strftime('time_%Y_%m_%d_%H_%M_%S')

class NoteFormat:
    def __init__(self,noteName:str = None):
        if noteName == None:
            noteName=get_time_str()
        #默认分组的id为0
        self.data = {"title":noteName,"content":"","create_at":None,"update_at":None,"category_id":0}

class SQLite3Conn:
    __conn = None
    __cursor = None
    def __init__(self,db_name:str=None):
        try:
            if db_name is None:
                self.__conn = connect(":memory:")
            else:
                if db_name[len(db_name) - 3:len(db_name)] != ".db":
                    db_name = db_name + ".db"
                self.__conn = connect(os.path.join("..", "Database", db_name))
            self.__cursor = self.__conn.cursor()
        except sqlite3.OperationalError as e:
            print(f"Failed to connect to database: {str(e)}")
        except sqlite3.Error as e:
            print(f"Failed to connect to database, known error: {str(e)}")
    def execute(self,sql:str):
        self.__cursor.execute(sql)
    def execute_args(self,sql:str,args:tuple):
        self.__cursor.execute(sql, args)
    def fetch(self,size:int=-1):
        if size <= 0:
            return self.__cursor.fetchall()
        elif size == 1:
            return self.__cursor.fetchone()
        else:
            return self.__cursor.fetchmany(size)
    def close(self):
        self.__conn.close()
