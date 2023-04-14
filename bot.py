import sqlite3 as sq

conn = sq.connect('database.db')
cur = conn.cursor()


class logs:  # le tableau des maintenances
    def __init__(self) -> None:  # creation de la table des maintenances
        cur.execute(
            "CREATE TABLE IF NOT EXISTS maintenances(id int NOT NULL, name , type, date_of_maintenance date,length int,owner,members DEFAULT '',risk_level int,risk_comment DEFAULT '',comment DEFAULT '',tags DEFAULT '')")

    def end(self):  # Closes connection
        conn.close()

    def add(name, type, date, length, owner, members, risk_lvl, risk_cmt='', comment='', tags=''):  # ajout d'une maintenance
        new_id = cur.execute(
            "SELECT max(id) from maintenances").fetchone()[0] + 1
        cur.execute(
            f"INSERT INTO maintenances VALUES ({new_id}, '{name}', '{type}','{date}',{length}, '{owner}', '{members}', {risk_lvl}, '{risk_cmt}','{comment}','{tags}')")
        conn.commit()

    def get(name):
        conn.commit()

    def edit(name, *edits):
        conn.execute()
        conn.commit()

    def add_user(self, name, user):
        conn.commit()

    def del_user(name, user):
        conn.commit()

    def delete(id):
        conn.execute(f'DELETE FROM maintenances WHERE id={id}')
        conn.commit()
