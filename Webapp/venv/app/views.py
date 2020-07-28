import os
from flask import Flask, render_template, request, redirect
from models import site_user, get_restaurant, get_review, suggestion_from_friend, get_category, get_business, get_photo, get_city
from py2neo import Graph
import requests
from hours import split_times
from datetime import datetime
from random import randint

app = Flask(__name__)
business = []

@app.route('/')
def home():
    graph = Graph("bolt://neo4j:group9@localhost:8000")
    c = get_category(graph)
    return render_template('search.html', category=c)


@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        graph = Graph("bolt://neo4j:group9@localhost:8000")
        c = get_category(graph)
        user_details = request.form
        city_split=user_details['city'].split(' ')
        newstr = ""
        for str in city_split:
            newstr+=str.capitalize()
        user = site_user(newstr.strip(), user_details['cuisine'], user_details['date'], user_details['appt'])
        restaurant = get_restaurant(graph, user)

        if restaurant != "No results found":
            bus, review_count = restaurant
            mainres = bus
            review = get_review(graph, bus['id'])
            bus_from_friend_stars = []

            if review != "No results found":
                reviewer_name, reviewer_id, review_stars = review
                business_from_friend = suggestion_from_friend(graph, reviewer_id, user_details['cuisine'], bus['id'])

                if business_from_friend !="No results found":
                    for b in business_from_friend:
                        business.append(b['b'])
                        bus_from_friend_stars.append(b['review_stars'])

        else:
            return redirect('/non_found')

        return render_template('res.html', srch=user, mainbus=mainres, businesses=business, friend_stars=bus_from_friend_stars, category=c, zip=zip)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/random", methods = ['POST', 'GET'])
def random():
    week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    city = get_city()
    date = week[datetime.today().weekday()]

    now = datetime.now()
    min = now.minute
    if min < 10:
        min = "0" + str(min)
    appt = "{}:{}".format(now.hour, min)

    graph = Graph("bolt://neo4j:group9@localhost:8000")
    c = get_category(graph)

    food = 'Restaurants'
    user_details = {
        'city': city,
        'cuisine': food,
        'date': date,
        'appt': appt
    }
    print(user_details)
    user = site_user(user_details['city'], user_details['cuisine'], user_details['date'], user_details['appt'])
    restaurant = get_restaurant(graph, user)

    if restaurant != "No results found":
        bus, review_count = restaurant
        mainres = bus
        review = get_review(graph, bus['id'])
        bus_from_friend_stars = []

        if review != "No results found":
            reviewer_name, reviewer_id, review_stars = review
            business_from_friend = suggestion_from_friend(graph, reviewer_id, user_details['cuisine'], bus['id'])

            if business_from_friend !="No results found":
                for b in business_from_friend:
                    business.append(b['b'])
                    bus_from_friend_stars.append(b['review_stars'])

    else:
        return redirect('/non_found')

    return render_template('res.html', srch=user, mainbus=mainres, businesses=business, friend_stars=bus_from_friend_stars, category=c, zip=zip)


@app.route("/result/<string:id>")
def profile(id):
    graph = Graph("bolt://neo4j:group9@localhost:8000")
    bus, reviews = get_business(graph, id)
    photos = get_photo(bus[0]['b']['id'], graph)

    return render_template("profile.html", bus=bus[0]['b'], review_count=bus[0]['review_count'], bus_reviews=reviews, photo=photos)

@app.route("/non_found")
def non_found():
    graph = Graph("bolt://neo4j:group9@localhost:8000")
    c=get_category(graph)
    return render_template("no_result.html", category=c)

if __name__ == '__main__':
    app.run(debug = True, port=5002)


