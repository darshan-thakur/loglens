from dotenv import load_dotenv
import os
import calendar
from sqlalchemy import (Column, DateTime, String, Text, create_engine, text)
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

class DBEngine:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
    
    # Get Handles

    def get_session(self):
        try:
            return self.Session()
        except:
            return None

    def execute_query(self, query):
        with self.engine.connect() as connection:
            result = connection.execute(query)
            return result.fetchall()
    
    #CRUD

    def insert_data(self, data_obj):
        session = self.get_session()
        try:
            session.add(data_obj)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
    
    def insert_multiple_data(self, data_obj_list):
        session = self.get_session()
        try:
            session.add_all(data_obj_list)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
          
    #Partitioning

    def create_partition_on_month(self, month : int, year : int):
        partition_name = f"logs_{month}_{year}"
        last_date = calendar.monthrange(year, month)

        create_partition_sql = f"""
        CREATE TABLE IF NOT EXISTS {partition_name}
        PARTITION OF logs
        FOR VALUES FROM ('{year}-{month}-01') TO ('{year}-{month}-{last_date}');
        """
        
        with self.engine.connect() as connection:
            connection.execute(text(create_partition_sql))
            print(f"Partition {partition_name} created.")

#TODO : Set this create_partition_on_month function in cron schedule monthly interval to create partition tables on main log table.

Base = declarative_base()

class Log(Base):
    __tablename__ = "logs"
    
    id = Column(String(40), primary_key=True)
    time = Column(DateTime, nullable=False, index=True)
    level = Column(String(50), nullable=False)
    component = Column(String(100))
    message = Column(Text, nullable=False)