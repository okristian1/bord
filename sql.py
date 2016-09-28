
from fetch import *

#restaurant_list = get_info()


conn = sqlite3.connect('bookings.db')
c = conn.cursor()


def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS bord(table_id TEXT PRIMARY KEY)")
    c.execute("CREATE TABLE IF NOT EXISTS reservations(id INTEGER PRIMARY KEY, table_id TEXT, db_booking_start DATETIME, db_booking_end DATETIME, db_booking_date TEXT, pax INTEGER, customer TEXT )")

def data_entry():
    c.execute('''INSERT INTO bord(table_id, chairs)
    VALUES
    ("Restaurant Eld 5", 2),
    ("Restaurant Eld 6", 2),
    ("Restaurant Eld 7", 2),
    ("Restaurant Eld 8", 2),
    ("Restaurant Eld 9", 2),
    ("Restaurant Eld 10", 8),
    ("Restaurant Eld 11", 2),
    ("Restaurant Eld 12", 2),
    ("Restaurant Eld 13", 2),
    ("Restaurant Eld 14", 2),
    ("Restaurant Eld 17", 8),
    ("Restaurant Eld 18", 6),
    ("Restaurant Eld 19", 6),
    ("Restaurant Eld 20", 8),
    ("Restaurant Eld 21", 2),
    ("Restaurant Eld 22", 2),
    ("Restaurant Eld 23", 2),
    ("Restaurant Eld 24", 2),
    ("Restaurant Eld 25", 4),
    ("Restaurant Eld 26", 4),
    ("Restaurant Eld 27", 4),
    ("Restaurant Eld 28", 4),
    ("Restaurant Eld 29", 6),
    ("Restaurant Eld 30", 6),
    ("Restaurant Eld 31", 2),
    ("Restaurant Eld 32", 4),
    ("Restaurant Eld 40", 16),
    ("Restaurant Eld 43", 8),
    ("Restaurant Eld 44", 10),
    ("Frati 10", 4),
    ("Frati 11", 4),
    ("Frati 13", 4),
    ("Frati 14", 4),
    ("Frati 16", 4),
    ("Frati 18", 4),
    ("Frati 19", 4),
    ("Frati 22", 4),
    ("Frati 23", 4),
    ("Frati 26", 4),
    ("Frati 27", 4),
    ("Frati 30", 4),
    ("Frati 36", 4),
    ("Frati 37", 4),
    ("Frati 43", 4),
    ("Frati 50", 4),
    ("Frati 51", 4),
    ("Frati 52", 4),
    ("Frati 53", 4),

    ''')

    conn.commit()


# Fetches all existing reservations from bookatable server and creates a new entry if it does not already exsist.
def add_new_reservations():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()

    counter = 0
    for restaurant in restaurant_list:
        for thing in restaurant:
            for reservation in thing:
                for i in reservation:
                    for g in reservation.get('TableNrs'):
                        while counter < len(reservation.get('TableNrs')):
                            restaurant = reservation.get('RestaurantName')
                            start_temp = (reservation.get('StartDateTime')[6:16])
                            db_booking_start = datetime.fromtimestamp(float(start_temp))
                            end_temp = (reservation.get('EndDateTime')[6:16])
                            db_booking_end = datetime.fromtimestamp(float(end_temp))
                            db_booking_date = datetime.fromtimestamp(int(start_temp)).strftime('%Y-%m-%d')
                            customer = reservation.get('CustomerName')
                            pax = reservation.get('NrOfGuest')
                            table_id = restaurant + ' ' + str(reservation.get('TableNrs')[counter])
                            new_reservation = [table_id, db_booking_start, db_booking_end, pax, customer]
                            counter+=1

                            c.execute("SELECT table_id FROM reservations WHERE table_id=? AND db_booking_start = ? AND db_booking_end = ? AND pax = ? AND customer = ?",(table_id, db_booking_start, db_booking_end, pax, customer))
                            #create new reservation if reservation in check but not in database
                            data = c.fetchone()
                            if data is None:
                                print ("Creating new reservation.")
                                c.execute('''INSERT INTO reservations(table_id, db_booking_start, db_booking_end, db_booking_date, pax, customer ) VALUES(?,?,?,?,?,?)''', (table_id, db_booking_start, db_booking_end, db_booking_date, pax, customer))

                        else:
                            pass
                counter=0

            conn.commit()
    c.close()
    conn.close()


# Loops over all reservations in local database and deletes them if they are noe longer found in bookatables database.

def delete_old():

    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()

    c.execute('''SELECT table_id, db_booking_start, db_booking_end, db_booking_date, pax, customer FROM reservations''')
    old = c.fetchall()
    new = []


    counter = 0
    for restaurant in restaurant_list:
        for thing in restaurant:
            for reservation in thing:
                for i in reservation:
                    for g in reservation.get('TableNrs'):
                        while counter < len(reservation.get('TableNrs')):
                            restaurant = reservation.get('RestaurantName')
                            start_temp = (reservation.get('StartDateTime')[6:16])
                            db_booking_start = str(datetime.fromtimestamp(float(start_temp)))
                            end_temp = (reservation.get('EndDateTime')[6:16])
                            db_booking_end = str(datetime.fromtimestamp(float(end_temp)))
                            db_booking_date = datetime.fromtimestamp(int(start_temp)).strftime('%Y-%m-%d')
                            customer = reservation.get('CustomerName')
                            pax = reservation.get('NrOfGuest')
                            table_id = restaurant + ' ' + str(reservation.get('TableNrs')[counter])
                            new_reservation = (table_id, db_booking_start, db_booking_end, db_booking_date, pax, customer)
                            new.append(new_reservation)
                            counter+=1
                counter = 0


    c.execute('''SELECT id FROM reservations ORDER BY ROWID ASC LIMIT 1 ''')
    rowid_get = c.fetchall()
    rowid_loop = [x[0] for x in rowid_get]
    rowid_counter = rowid_loop[0] -1

    for row in old:
        rowid_counter += 1
        if row not in new:
            print ("Reservation not found. Deleting")
            c.execute("DELETE FROM reservations WHERE id = ?", (rowid_counter,));
            conn.commit()

    c.close()
    conn.close()



create_table()
data_entry()
#add_new_reservations()
#delete_old()


c.close()
conn.close()
