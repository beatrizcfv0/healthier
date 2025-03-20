# Beatriz CFV
# March 2025

import sqlite3
import re
import pandas as pd # type: ignore

def main():
    # Connection to your own database
    connection = sqlite3.connect('data/personal_data.db')
    cursor = connection.cursor()

    cursor.execute('DROP TABLE IF EXISTS sleep') # Delete table if needed
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sleep (
        date TEXT PRIMARY KEY, 
        deep REAL,
        light REAL,
        rem REAL,
        total REAL
        )
    ''')


    # Functions
    def get_minutes(input):
        while True:
            match = re.search(r"(\d+)\s*h\s*(\d+)\s*min", input) # regex
            if match:
                hours = int(match.group(1))
                minutes = int(match.group(2))
                total = hours * 60 + minutes
                return total
            else:
                print("Invalid time format.")
                input = input('Try again: ')


    date = input('Date (DD/MM/YY): ')
    print('IE: (Xh Ymin)')

    deep = get_minutes(input('Deep sleep: '))
    light = get_minutes(input('Light sleep: '))
    rem = get_minutes(input('REM sleep: '))

    total_minutes = deep + light + rem
    total = round((total_minutes) / 60, 2)

    deep = round((deep / total_minutes) * 100, 2)
    light = round((light / total_minutes) * 100, 2)
    rem = round((rem / total_minutes) * 100, 2)

    # Insert data
    cursor.execute('''
        INSERT OR REPLACE INTO sleep (date, deep, light, rem, total)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, deep, light, rem, total))

    connection.commit()
    df = pd.read_sql_query('SELECT * FROM sleep', connection)
    df.to_excel('sleep_data.xlsx', index=False)

    cursor.execute('SELECT * FROM sleep ORDER BY date DESC')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    connection.close()

    print('+-------------+-----+    +-------------+--------+')
    print(f'+ Light sleep + 55% +    + Light sleep + {light}% +')
    print('+-------------+-----+    +-------------+--------+')
    print(f'+  Deep sleep + 23% +    +  Deep sleep + {deep}% +')
    print('+-------------+-----+    +-------------+--------+')
    print(f'+  REM sleep  + 22% +    +  REM sleep  + {rem}% +')
    print('+-------------+-----+    +-------------+--------+')


if __name__ == '__main__':
    main()
