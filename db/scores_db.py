import mysql.connector


def sql_connect():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
    )

    cur = con.cursor()

    query = "create database if not exists flappybird"
    cur.execute(query)

    query = "use FlappyBird"
    cur.execute(query)

    query = "create table if not exists scores(ID int primary key AUTO_INCREMENT,Score int, Difficulty varchar(10), Date date)"
    cur.execute(query)
    con.commit()

    return con, cur


def score_upload(SCORE, DIFFICULTY, DATE):
    con, cur = sql_connect()

    query = f"insert into scores (Score, Difficulty, Date) values ({SCORE}, '{DIFFICULTY}', '{DATE}')"
    cur.execute(query)

    con.commit()

    con.close()


def highscore(difficulty):
    con, cur = sql_connect()

    query = f"select max(Score) from scores group by Difficulty having Difficulty = '{difficulty}'"
    cur.execute(query)

    highest = cur.fetchone()[0]

    con.close()

    return highest
