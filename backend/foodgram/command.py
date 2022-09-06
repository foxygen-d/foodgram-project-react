import csv, sqlite3


con = sqlite3.connect('/home/foxygen/Dev/foodgram-project-react/backend/foodgram/db.sqlite3')
cur = con.cursor()
# cur.execute("CREATE TABLE t (id, name, amount, measurement_unit);") # название таблицы в БД и колонки прописать вручную

with open('/home/foxygen/Dev/foodgram-project-react/data/ingredients.csv','r') as fin: # поменять на путь до файла csv
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['name'], i['measurement_unit']) for i in dr] # названия колонок

cur.executemany("INSERT INTO posts_ingredient (id, name, measurement_unit) VALUES (?, ?, ?);", to_db) # название таблицы в БД и колонки прописать вручную. ? должны совпадать с кол-ом колонок
con.commit()
con.close()