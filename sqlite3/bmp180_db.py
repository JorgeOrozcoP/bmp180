import sqlite3
import os

class bmp180_sqlite3:

    def __init__(self, device):
        self.con = sqlite3.connect(os.path.dirname(__file__) + "/bmp180.db")
        self.cursor = self.con.cursor()
        self.device = device


    def create_db(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS bmp180_readings("
                            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "temperature_data NUMERIC, "
                            "pressure_data NUMERIC, "
                            "measurement_datetime DATETIME, "
                            "device TEXT);")
        self.con.commit()


    def close_db(self):
        self.con.close()


    def insert(self, temp, pressure):
        assert float(temp) == True
        assert float(pressure) == True

        self.cursor.execute(f"INSERT INTO bmp180_readings(temperature_data, "
                             "pressure-data, measurement_datetime, device) "
                             'VALUES (?, ?, datetime("now"),?;',
                             (temp, pressure, self.device))
        self.con.commit()


    def get_1_row(self):
        self.cursor.execute("select * from bmp180_readings limit 1;")
        return self.cursor.fetchall()

    def get_last_n_rows(self, n):
        self.cursor.execute("SELECT * FROM bmp180_readings ORDER BY measurement_datetime"
                            " ASC LIMIT ?;", (n))
        return self.cursor.fetchall()



if __name__ == "__main__":
    sql = bmp180_sqlite3("test")
    sql.create_db()
    print(sql.get_1_row())
    sql.con.close()
