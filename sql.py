
from fetch import *

restaurant_list = get_info()


conn = sqlite3.connect('bookings.db')
c = conn.cursor()


def create_table():
    # MAKE TABLES FOR ALL THE RESTAURANTS
    c.execute("CREATE TABLE IF NOT EXISTS bord(table_id TEXT PRIMARY KEY)")
    # MAKE TABLE WHERE ALL RESERVATIONS ARE STORED. TABLE ID IS NOT UNIQUE HERE BECAUSE ONE TABLE CAN HAVE MULTIPLE RESERVATIONS
    c.execute("CREATE TABLE IF NOT EXISTS reservations(id INTEGER PRIMARY KEY, table_id TEXT, db_booking_start DATETIME, db_booking_end DATETIME, pax INTEGER, customer TEXT )")

    # SEMI AUTOMATIC ENTRY OF table_id FROM RESTAURANTS.
def data_entry():
    restaurant = "SpareBank 1 "
    for i in range(200,202):
        c.execute('''INSERT INTO bord(table_id)
                          VALUES(?)''', (restaurant + str(i),))


    conn.commit()

# MAIN FUNCTION FOR UPDATING THE DATABASE. ONLY INSERTS NEW ROW IF IT DOES NOT ALREADY EXIST
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
                                c.execute('''INSERT INTO reservations(table_id, db_booking_start, db_booking_end, pax, customer ) VALUES(?,?,?,?,?)''', (table_id, db_booking_start, db_booking_end, pax, customer))

                            else:
                                print('Reservation found')
                        else:
                            pass
                counter=0

            conn.commit()
    c.close()
    conn.close()



def delete_old():

    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()

    c.execute('''SELECT table_id, db_booking_start, db_booking_end, pax, customer FROM reservations''')
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
                            start_temp = int(reservation.get('StartDateTime')[6:16]) + 7200
                            db_booking_start = ((start_temp - datetime(1970, 1, 1)) / timedelta(seconds=1))
                            end_temp = int(reservation.get('EndDateTime')[6:16]) + 7200
                            db_booking_end = ((end_temp - datetime(1970, 1, 1)) / timedelta(seconds=1))
                            customer = reservation.get('CustomerName')
                            pax = reservation.get('NrOfGuest')
                            table_id = restaurant + ' ' + str(reservation.get('TableNrs')[counter])
                            table_id = restaurant + ' ' + str(reservation.get('TableNrs')[counter])
                            new_reservation = (table_id, db_booking_start, db_booking_end, pax, customer)
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

        else:
            print ("found")
    c.close()
    conn.close()



create_table()
#get_info()
#data_entry()
add_new_reservations()
#delete_old()
#read_from_db(1461823200, 1461877200, '2016-04-28%', 'SpareBank 1%')


c.close()
conn.close()
