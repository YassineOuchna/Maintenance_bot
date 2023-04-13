import sqlite3 as sq

conn = sq.connect('database.db')
cur = conn.cursor()


class logs:  # le tableau des maintenances
    def __init__(self) -> None:  # creation de la table des maintenances
        cur.execute(
            "CREATE TABLE IF NOT EXISTS maintenances(id int NOT NULL, name , type, date_of_maintenance date,length int,owner,members,risk_lvl int,risk_cmt DEFAULT '',comment DEFAULT '',tags DEFAULT '')")

    def end(self):
        conn.close()

    def add(name, type, date, length, owner, members, risk_lvl, risk_cmt='', comment='', tags=''):  # ajout d'une maintenance
        new_id = cur.execute(
            "SELECT max(id) from maintenances").fetchone()[0] + 1
        cur.execute(
            f"INSERT INTO maintenances (id, name) VALUES ({new_id}, '{name}')")
        conn.commit()

    def get(name):
        conn.commit()

    def edit(name, *edits):
        conn.commit()

    def add_user(self, name, user):
        conn.commit()

    def del_user(name, user):
        conn.commit()

    def delete(name):
        conn.commit()


logs.add('test_row', 'test_ugh', '13-04-2023', 0.5, 'me', 'me', 0, 0)
