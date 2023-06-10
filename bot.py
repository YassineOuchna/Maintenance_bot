import sqlite3 as sq

conn = sq.connect('database.db')
cur = conn.cursor()


class logs:  # le tableau des maintenances
    def __init__(self) -> None:  # creation de la table des maintenances
        cur.execute(
            "CREATE TABLE IF NOT EXISTS maintenances(id int NOT NULL, name , type, date_of_maintenance date,length int,owner,members DEFAULT '',risk_lvl int,risk_cmt DEFAULT '',comment DEFAULT '',tags DEFAULT '')")

    def end(self):  # Closes connection
        conn.close()

    def add(name, type, date, length, owner, members, risk_lvl, risk_cmt='', comment='', tags=''):  # ajout d'une maintenance
        new_id = cur.execute(
            "SELECT max(id) from maintenances").fetchone()[0] + 1
        cur.execute(
            f"INSERT INTO maintenances VALUES ({new_id}, '{name}', '{type}','{date}',{length}, '{owner}', '{members}', {risk_lvl}, '{risk_cmt}','{comment}','{tags}')")
        conn.commit()

    def get(id):
        r = cur.execute(
            f"SELECT id, name, type, date_of_maintenance, length, owner, members, risk_lvl, risk_cmt, comment, tags FROM maintenances WHERE id={id}").fetchall()
        conn.commit()
        return r

    def edit(id, *edits):  # Takes multiple arguments, each argument is a couple (column,new_value)
        for (column, new_value) in edits:
            if type(new_value) == int:
                conn.execute(
                    f"UPDATE maintenances set {column}={new_value} WHERE id={id}")
            else:
                conn.execute(
                    f"UPDATE maintenances set {column}='{new_value}' WHERE id={id}")
        conn.commit()

    def add_user(id, user):
        old_members = cur.execute(
            f"SELECT members FROM maintenances WHERE id={id}").fetchone()[0]
        # using - as a seperator for easy access later on
        new_members = old_members + '-' + user
        cur.execute(
            f"UPDATE maintenances set members = '{new_members}' WHERE id={id}")
        conn.commit()

    def del_user(id, user):
        old_members = cur.execute(
            f"SELECT members FROM maintenances WHERE id={id}").fetchone()[0]
        new_members = ''
        for string in old_members.split('-'):
            if string != user:
                if len(new_members) == 0:
                    new_members += string
                else:
                    new_members += '-' + string
        cur.execute(
            f"UPDATE maintenances set members = '{new_members}' WHERE id={id}")
        conn.commit()

    def delete(id):
        conn.execute(f'DELETE FROM maintenances WHERE id={id}')
        conn.commit()
