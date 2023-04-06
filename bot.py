import sqlite3 as sq

conn = sq.connect('database.db')


class bot:
    def __init__(self) -> None:
        pass

    def add(self, name, type, date, length, members, risk_lvl, risk_cmt, comment, tags, owner):  # ajout d'une maintenance
        pass

    def get(self, name):
        pass

    def edit(self, name, *what_to_edit):
        pass

    def add_user(self, name, user):
        pass

    def del_user(self, name, user):
        pass

    def delete(self, name):
        pass
