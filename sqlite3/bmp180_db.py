import sqlite3
import os

class bmp180_sqlite3:

    def __init__(self, device):
        self.con = sqlite3.connect(os.path.dirname(__file__) + "/bmp180.db")
        self.cursor = self.con.cursor()
        self.device = device

    def insert(self, temp, pressure):
        assert float(temp) == True
        assert float(pressure) == True

        self.cursor.execute(f"INSERT INTO bmp180_readings(temperature_data, " \
                             "pressure-data, datetime, device) VALUES (?, ?, "\
                             'datetime("now"),?;', (temp, press, self.device))
        self.con.commit()


    def get_1_row(self):
        self.cursor.execute("select * from bmp180_readings limit 1;")
        return self.cursor.fetchall()

    def get_last_n_rows(self, n):
        self.cursor.execute("SELECT * FROM bmp180_readings ORDER BY datetime" \
                            " ASC LIMIT ?;", (n))
        return self.cursor.fetchall()



if __name__ == "__main__":
    sql = bmp180_sqlite3("test")
    print(sql.get_1_row())
    sql.con.close()
