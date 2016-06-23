# -*- coding: utf-8 -*-

from fetch import *
from descriptions import *

app = Flask(__name__)
app.secret_key = 'development'


@app.route('/kontakt')
def kontakt():
    return render_template("kontakt.html")


@app.route('/')
def my_form():
    return render_template("dev.html")

@app.route('/', methods=['POST'])
def my_form_post():

    get_time = request.form['selected_dt']
    get_sit_time = request.form['sit_time']
    temp = datetime.strptime(get_time, '%Y-%m-%d %H:%M')
    date = temp.date()
    b_start = ((temp - datetime(1970, 1, 1)) / timedelta(seconds=1))
    b_end = (b_start) + 3600 * int(get_sit_time)
    print (int(b_start))
    print (int(b_end))
    guests = request.form['guests']
    print (guests)
    print (get_sit_time)
    free_tables_banksalen = read_from_db(int(b_start), b_end , date, "SpareBank 1%")
    free_tables_aisuma = read_from_db(b_start, b_end, date, "AiSuma%")
    free_tables_frati = read_from_db(b_start, b_end, date, "Frati%")
    free_tables_eld = read_from_db(b_start, b_end, date, "Restaurant Eld%")
    free_tables_sostrenekarlsen = read_from_db(b_start, b_end, date, "Søstrene Karlsen%")
    free_tables_una = read_from_db(b_start, b_end, date, "Una Pizzeria e Bar%")

    restaurants = []

    if free_tables_banksalen >= int(guests)/4:
        restaurants.append({'id': "0", 'name': "Banksalen", 'link': "https://sparbank1.2book.se/", 'number': "970 61 815", 'description': description_banksalen, 'description_short': description_banksalen_short, 'kart': "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d7138.341521092942!2d10.4000946!3d63.4303828!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xf3f84bbb808078b7!2sBanksalen+Restaurant!5e0!3m2!1sno!2sno!4v1464779391998"})
    if free_tables_frati >= int(guests)/4:
        restaurants.append({'id': "1", 'name': "Frati", 'link': "https://frati.2book.se/", 'number': "735 25 733", 'description': description_frati, 'description_short': description_frati_short, 'kart': "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d7784.602155872907!2d10.392700778892342!3d63.429701070637456!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x7f00e8dd6ee4efc!2sFrati+restaurant!5e0!3m2!1sno!2sno!4v1464689729492"})
    if free_tables_aisuma >= int(guests)/4:
        restaurants.append({'id': "2", 'name': "AiSuma", 'link': "http://frati.2book.se/public/AiSuma", 'number': "735 49 271", 'description': description_aisuma, 'description_short': description_aisuma_short, 'kart': "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d7137.882528599673!2d10.4039798!3d63.4322252!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xb616a26176d651ea!2sAiSuma+Restaurant!5e0!3m2!1sno!2sno!4v1464699917650"})
    if free_tables_sostrenekarlsen > int(guests)/4:
        restaurants.append({'id': "3", 'name': "SøstreneKarlsen", 'link': "https://sostrenekarlsen.2book.se/", 'number': "736 00 025", 'description': description_søstrenekarlsen, 'description_short': description_søstrenekarlsen_short, 'kart': "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d7137.228880057128!2d10.4108471!3d63.4348489!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x7a454e0b5dbcc45!2sS%C3%B8strene+Karlsen+AS!5e0!3m2!1sno!2sno!4v1464767160518"})
    if free_tables_eld >= int(guests)/4:
        restaurants.append({'id': "4", 'name': "Eld", 'link': "http://eld.2book.se/public/EldRestaurant", 'number': "479 31 000", 'description': description_eld, 'description_short': description_eld_short,'kart': "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d7138.14416319743!2d10.39161!3d63.431175!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xd689dd7cc533ceb9!2sEld+Restaurant+%26+Bar!5e0!3m2!1sno!2sno!4v1464716916509"})
    if free_tables_una >= int(guests)/4:
        restaurants.append({'id': "5", 'name': "Una", 'link': "http://eld.2book.se/public/UnaPizzeria", 'number': "400 07 003", 'description': description_una, 'description_short': description_una_short,'kart': "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d7137.128179431432!2d10.410419!3d63.4352531!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x6849647bda4553c6!2sUna+pizzeria+e+bar!5e0!3m2!1sno!2sno!4v1465821401392"})


    elif restaurants == []:
        flash('Ingen ledige restauranter')
        return redirect(url_for('my_form_post'))


    return render_template('dev.html', restaurants = restaurants)


    # VALUES FOR tables_db AND reservations_db IS FROM list_of_restaurant_tables
def read_from_db(b_start, b_end, date, restaurant):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("""
    SELECT table_id FROM reservations WHERE ddate LIKE ? AND table_id LIKE ? AND NOT (? BETWEEN starting AND ending)
    UNION
    SELECT DISTINCT table_id FROM bord WHERE table_id LIKE ? AND table_id Not IN (SELECT DISTINCT table_id FROM reservations WHERE ddate LIKE ?)

    """, (date, restaurant, b_start, restaurant, date))


    data = c.fetchall()
    for row in data:
        print (row)
    return len(data)

    c.close()
    conn.close()



if __name__ == '__main__':
    app.run()
