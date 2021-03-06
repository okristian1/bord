# -*- coding: utf-8 -*-

from fetch import *
mail = Mail()


app = Flask(__name__)
#app.secret_key = "secret_key"

#app.config["MAIL_SERVER"] = "smtp.gmail.com"
#app.config["MAIL_PORT"] = 465
#app.config["MAIL_USE_SSL"] = True
#app.config["MAIL_USERNAME"] = 'okristian1@gmail.com'
#app.config["MAIL_PASSWORD"] = app_mail_password

#mail.init_app(app)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('Alle felter må fylles inn!')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=['okristian1@gmail.com'])
      msg.body = """
      Melding fra %s
      Epost: %s;
      Emne: %s
      Melding: %s
      """ % (form.name.data, form.email.data, form.subject.data, form.message.data)
      mail.send(msg)

      return render_template('contact.html', success=True)

  elif request.method == 'GET':
    return render_template('contact.html', form=form)


@app.route('/')
def my_form():
    return render_template("dev.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contactform')
def contactform():
    return render_template("contact.html")




@app.route('/', methods=['POST'])
def my_form_post():
    if request.method == 'POST':
        get_time = request.form['selected_dt']
        get_sit_time = request.form['sit_time']
        user_timedate_start = datetime.strptime(get_time, '%Y-%m-%d %H:%M')
        user_timedate_end = user_timedate_start + timedelta(hours=int(get_sit_time))
        print (user_timedate_start)
        print (user_timedate_end)
        user_date = user_timedate_start.date()
        guests = request.form['guests']
        free_tables_aisuma = read_from_db(user_timedate_start, user_timedate_end, user_date, "AiSuma%", guests)
        free_tables_frati = read_from_db(user_timedate_start, user_timedate_end, user_date, "Frati%", guests)
        free_tables_eld = read_from_db(user_timedate_start, user_timedate_end, user_date, "Restaurant Eld%", guests)
        free_tables_una = read_from_db(user_timedate_start, user_timedate_end, user_date, "Una Pizzeria e Bar%", guests)
        free_tables_sostrenekarlsen = read_from_db(user_timedate_start, user_timedate_end, user_date, "Søstrene Karlsen%", guests)

        restaurants = []

        if free_tables_frati:
            restaurants.append({
            'id': "1",
            'name': "Frati",
            'logo': "static/media/img/logo_Frati",
            'link': "http://frati.2book.se/public/NyeFrati",
            'number': "735 25 733",
            'description': description_frati,
            'kart': "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d7784.602155872907!2d10.392700778892342!3d63.429701070637456!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x7f00e8dd6ee4efc!2sFrati+restaurant!5e0!3m2!1sno!2sno!4v1464689729492"})
        if free_tables_aisuma:
            restaurants.append({
            'id': "2",
            'name': "AiSuma",
            'logo': "static/media/img/logo_Aisuma",
            'link': "http://frati.2book.se/public/AiSuma",
            'number': "735 49 271",
            'description': description_aisuma,
            'kart': "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d7137.882528599673!2d10.4039798!3d63.4322252!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xb616a26176d651ea!2sAiSuma+Restaurant!5e0!3m2!1sno!2sno!4v1464699917650"})
        if free_tables_eld:
            restaurants.append({
            'id': "4",
            'name': "Eld",
            'logo': "static/media/img/logo_eld",
            'link': "https://eld.2book.se/public/EldRestaurant",
            'number': "479 31 000",
            'description': description_eld,
            'kart': "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d7138.14416319743!2d10.39161!3d63.431175!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xd689dd7cc533ceb9!2sEld+Restaurant+%26+Bar!5e0!3m2!1sno!2sno!4v1464716916509"})
        if free_tables_una:
            restaurants.append({
            'id': "5",
            'name': "Una",
            'logo': "static/media/img/logo_una.jpeg",
            'link': "http://frati.2book.se/public/UnaPizzeria",
            'number': "400 07 003",
            'description': description_una,
            'kart': "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d7137.128179431432!2d10.410419!3d63.4352531!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x6849647bda4553c6!2sUna+pizzeria+e+bar!5e0!3m2!1sno!2sno!4v1465821401392"})
        if free_tables_sostrenekarlsen:
            restaurants.append({
            'id': "3",
            'name': "SøstreneKarlsen",
            'logo': "static/media/img/logo_søstrenekarlsen.jpeg",
            'link': "https://sostrenekarlsen.2book.se/",
            'number': "736 00 025",
            'description': description_sostrenekarlsen,
            'kart': "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d7137.228880057128!2d10.4108471!3d63.4348489!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x7a454e0b5dbcc45!2sS%C3%B8strene+Karlsen+AS!5e0!3m2!1sno!2sno!4v1464767160518"})

        elif restaurants == []:
            flash("Beklager, fant ingen restauranter med ledig bord!")
            return render_template('dev.html')


        return render_template('restaurants.html', restaurants = restaurants)


# Finds available restaurant tables. User = website selected. db = existing database info.
# Selects all tables with enough chairs that are free within the timedate selected.
def read_from_db(user_timedate_start, user_timedate_end, user_date, restaurant, guests):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('''
    SELECT distinct table_id from bord where (chairs >= ?) and table_id like ? and table_id not in
    (select distinct table_id from reservations where db_booking_date = ?)
    UNION
    SELECT table_id FROM reservations WHERE table_id LIKE ? AND db_booking_date = ? AND table_id NOT IN
    (SELECT table_id from reservations WHERE (db_booking_start <= ?) and (? <= db_booking_end))
    ''', (guests, restaurant, user_date, restaurant, user_date, user_timedate_end, user_timedate_start))

    data = c.fetchall()
    return data

    c.close()
    conn.close()



if __name__ == '__main__':
    app.run()
