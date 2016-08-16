# -*- coding: utf-8 -*-
import os
from flask import Flask, session, render_template, g, request, flash, redirect, url_for
import requests
import json
import sys
from urllib.request import urlopen
import time
import datetime
from datetime import datetime, timedelta
import calendar
from time import mktime
import codecs
import sqlite3
from flask_mail import Mail, Message
from config import *
from forms import ContactForm
from descriptions import *



def get_info():

#    reservations_banksalen = []
    reservations_aisuma = []
    reservations_frati = []
    reservations_eld = []
    reservations_sostrenekarlsen = []
    reservations_una = []

    date = datetime.now().date() - timedelta(days=1)
    for i in range(30):
        date += timedelta(days=1)

#        banksalen = urlopen('https://sparbank1.2book.se/simpleIntegration/GetCreaJson?RestaurantId=4&dateTime=' + str(date))
        aisuma = urlopen('https://frati.2book.se/simpleIntegration/GetCreaJson?RestaurantId=3&dateTime=' + str(date))
        frati = urlopen('https://frati.2book.se/simpleIntegration/GetCreaJson?RestaurantId=1&dateTime=' + str(date))
        eld = urlopen('https://eld.2book.se/simpleIntegration/GetCreaJson?RestaurantId=4&dateTime=' + str(date))
        sostrenekarlsen = urlopen('https://sostrenekarlsen.2book.se/simpleIntegration/GetCreaJson?RestaurantId=4&dateTime=' + str(date))
        una = urlopen ('https://frati.2book.se/simpleIntegration/GetCreaJson?RestaurantId=5&dateTime=' +str(date))
        #initialise reader
        reader = codecs.getreader("utf-8")
        # Store data in variables
#        reservations_banksalen.append(json.load(reader(banksalen)))
        reservations_aisuma.append(json.load(reader(aisuma)))
        reservations_frati.append(json.load(reader(frati)))
        reservations_eld.append(json.load(reader(eld)))
        reservations_sostrenekarlsen.append(json.load(reader(sostrenekarlsen)))
        reservations_una.append(json.load(reader(una)))

    restaurant_list = [reservations_frati, reservations_aisuma, reservations_sostrenekarlsen, reservations_eld, reservations_una]

    return restaurant_list
