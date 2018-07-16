import postgresql

#Создание новой записи в таблицу session_log
def insertIntoLogSession(screen_area,hand):
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.prepare("insert into session_log(screen_area,hand) values($1,$2)")
    data(screen_area,hand)

#Получение значение поля action последней записи для текущей области экрана
def getLastRowActionFromLogSession(area):
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("select trim(action) as action from session_log where area = " + area + " order by id desc limit 1")
    return data

#Обновление значения поля action последней записи для текущей области экрана
def updateActionLogSession(action, area):
    db = postgresql.open('pq://postgres:postgres@localhost:5433/postgres')
    data = db.query("update session_log set action = " + action + " where screen_area = " + area + " order by id desc limit 1")