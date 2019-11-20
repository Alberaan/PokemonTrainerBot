import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, exc, update
from sqlalchemy.orm import scoped_session, sessionmaker

def get_engine():
    url = os.getenv("DATABASE_URL")
    engine = create_engine(url)
    #db = scoped_session(sessionmaker(bind=engine))

    return engine
   
def delete_tables():
    engine = get_engine()

    sql = 'DROP TABLE IF EXISTS stats;'
    result = engine.execute(sql)

def create_table():
    engine = get_engine()
    meta = MetaData()
    
    stats = Table('stats', meta,
        Column("chat_id", Integer, primary_key=True), 
        Column("acero", Integer, default=0), 
        Column("agua", Integer), 
        Column("bicho", Integer), 
        Column("dragón", Integer), 
        Column("eléctrico", Integer), 
        Column("fantasma", Integer), 
        Column("fuego", Integer), 
        Column("hada", Integer), 
        Column("hielo", Integer), 
        Column("lucha", Integer), 
        Column("normal", Integer), 
        Column("planta", Integer), 
        Column("psíquico", Integer), 
        Column("roca", Integer), 
        Column("siniestro", Integer), 
        Column("tierra", Integer), 
        Column("veneno", Integer), 
        Column("volador", Integer) 
        )
    meta.create_all(engine)

def insert_new_stats(newChatId):
    engine = get_engine()
    m = MetaData()

    tableToInsert = get_table_by_name("stats")
    ins = tableToInsert.insert().values(chat_id=newChatId, acero=0, agua=0, bicho=0, dragón=0, eléctrico=0, fantasma=0, fuego=0, hada=0, hielo=0, lucha=0, normal=0, planta=0, psíquico=0, roca=0, siniestro=0, tierra=0, veneno=0, volador=0)

    conn = engine.connect()
    try:
        result = conn.execute(ins)
    except exc.IntegrityError:
        pass

def get_table_by_name(name):
    engine = get_engine()
    meta = MetaData()
    meta.reflect(bind=engine)

    return meta.tables[name]

def get_stats_from_db(myChatId):
    create_table()
    engine = get_engine()
    stats = []

    tableToSelect = get_table_by_name("stats")
    query = tableToSelect.select().where(tableToSelect.c.chat_id==myChatId)

    conn = engine.connect()
    results = conn.execute(query)

    text = ""
    for row in results:
        text += str(row) + "\n"
    
    return text

def list_tables():
    engine = get_engine()
    m = MetaData()
    m.reflect(engine)

    for table in m.tables.values():
        print(table.name)
        for column in table.c:
            print(column.name)

def update_stats(myChatId, value1, value2, rightOrWrong):
    quantityToChange = ""
    if rightOrWrong == "right":
        quantityToChange = "+1"
    if rightOrWrong == "wrong":
        quantityToChange = "-1"

    stats = get_table_by_name("stats")

    engine = get_engine()

    query1 = "UPDATE stats set " + value1.lower() +" = " + value1.lower() + " + " + quantityToChange + " where chat_id = " + str(myChatId)
    result = engine.execute(query1)

    if result.rowcount == 0:
        insert_new_stats(myChatId)
        query1 = "UPDATE stats set " + value1.lower() +" = " + value1.lower() + " + " + quantityToChange + " where chat_id = " + str(myChatId)
        result = engine.execute(query1)

    query1 = "UPDATE stats set " + value2.lower() +" = " + value2.lower() + " + " + quantityToChange + " where chat_id = " + str(myChatId)
    result = engine.execute(query1)

def delete_my_stats(myChatId):
    engine = get_engine()
    stats = get_table_by_name("stats")
    query = stats.delete().where(stats.c.chat_id==myChatId)
    result = engine.execute(query)
    result = insert_new_stats(myChatId)
