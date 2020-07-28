from datetime import date, datetime, timedelta
from py2neo import Graph
from hours import split_times
import json
import requests
from bs4 import BeautifulSoup
import geoip2.database as geo

class site_user:
    def __init__(self, city, category, day, hours):
        self.city = city
        self.category = category
        self.day = day
        self.hours = hours


def get_review(graph, res_id):
    params={}
    params['today'] = date.today()
    params['durationlimit'] = datetime(date.today().year - 2, date.today().month, date.today().day)
    result = graph.run("MATCH (u:User)-[r:REVIEWS]->(b:Business) WHERE b.id='{}' WITH r.useful as Use,u,r "
                       "WHERE r.date in [$durationlimit, $today] "              
                       "RETURN "
                       "u.name as name,"
                       "u.id as ID, "
                       "r.date as date, "
                       "r.text as text, "
                       "r.stars as stars, "
                       "r.useful as useful "
                       "ORDER BY Use DESC, date DESC "
                       "LIMIT 3 ".format(res_id), params).data()

    if len(result) == 0:
        result = graph.run("MATCH (u:User)-[r:REVIEWS]->(b:Business) WHERE b.id='{}' WITH r.useful as Use,u,r "
                           "RETURN "
                           "u.name as name, "
                           "u.id as ID, "
                           "r.date as date, "
                           "r.text as text, "
                           "r.stars as stars "
                           "ORDER BY Use, date DESC "
                           "LIMIT 3 ".format(res_id)).data()
    if len(result)==0:
        return "No results found"

    return result[0]['name'], result[0]['ID'], result[0]['stars']

def get_restaurant(graph, user):

    results = graph.run("MATCH (r:Business)-[:IN_CATEGORY]->(c:Category) WHERE c.id='{}' AND r.city='{}'"
                        " AND r.is_open = true"
                        " RETURN r.id AS ID"
                        " ORDER BY r.stars DESC".format(user.category, user.city)).data()

    params = {}
    params['resultlist'] = [r['ID'] for r in results]
    most_count = graph.run("MATCH (b:Business) WITH  b, SIZE((:User)-[:REVIEWS]->(b)) as review_count "
                           "WHERE b.id in $resultlist "
                           "RETURN b AS Restaurant, review_count"
                           " ORDER BY Restaurant.stars DESC, review_count DESC LIMIT 10 ", params).data()  # Thanks StackOverflow!
    result = most_count

    result_list = []
    for r in result:
        if r['Restaurant']['hours'] != None:
            times = r['Restaurant']['hours'][1:len(r['Restaurant']['hours'])-1]
            time_list = split_times(times)

            for t in time_list:
                open_time = datetime.strptime(t[1], "%H:%M")
                close_time = datetime.strptime(t[2], "%H:%M")
                if user.day == t[0]:
                    if open_time >= close_time:
                        close_time += timedelta(hours=24)

                    if datetime.strptime(user.hours,"%H:%M") >= open_time and datetime.strptime(user.hours, "%H:%M") <= close_time:
                        result_list.append(r)

    if len(result_list)==0:
        return "No results found"

    return result_list[0]['Restaurant'], result_list[0]['review_count']

def suggestion_from_friend(graph, user_id, category, res_id):
    # And friends of friends

    list_of_friends = graph.run(
        "MATCH (u:User)-[:FRIEND*1..2]->(f:User) WHERE u.id = '{}' AND f <> u "
        "WITH u,f, "
        "SIZE((f:User)-[:REVIEWS]->(:Business)) as num_reviews "
        "ORDER BY num_reviews DESC LIMIT 50 "
        "MATCH (f)-[r:REVIEWS]->(b:Business)-[:IN_CATEGORY]->(c:Category) "
        "WITH avg(r.stars) AS stars, b, c "
        "WHERE c.id = '{}' AND b.id <> '{}' "
        "RETURN b, stars as review_stars "
        "ORDER BY review_stars DESC LIMIT 5".format(user_id, category, res_id)).data()

    result = list_of_friends

    if len(result)==0:
        return "No results found"

    return result

def get_category(graph):
    return graph.run("MATCH (c:Category) WHERE c.id in ['Specialty Food', 'Restaurants', 'Dim Sum', 'Imported Food', "
                     "' Food', 'Chinese', 'Ethnic Food', 'Seafood', 'Sushi Bars', 'Japanese', 'Mexican', 'Tacos',"
                     " 'Tex-Mex', 'Fast Food', 'Italian', 'Pizza', 'Chicken Wings', 'Bakeries', 'Burgers',"
                     " 'Comfort Food', 'Juice Bars & Smoothies', 'Vegan', 'Tapas Bars', 'Southern',"
                     " 'Coffee & Tea', 'Ice Cream & Frozen Yogurt', 'American (Traditional)', 'American (New)',"
                     " 'Steakhouses', 'Food Banks', 'Desserts', 'Persian/Iranian', 'Fish & Chips', 'Korean', 'Cafes',"
                     " 'Canadian (New)', 'Mediterranean', 'Donuts', 'Butcher', 'Vietnamese', 'Thai',"
                     " 'Hot Dogs', 'Vegetarian', 'Soup', 'Buffets', 'Diners' ] RETURN c.id AS ID").data()

def get_business(graph, id):
    business =  graph.run("MATCH (b:Business) WHERE b.id='{}' WITH b, SIZE((:User)-[:REVIEWS]->(b)) as review_count "
              " return b, review_count".format(id)).data()

    reviews = graph.run("MATCH (u:User)-[r:REVIEWS]->(b:Business) WHERE b.id='{}' AND exists(r.useful) WITH r.useful as Use,u,r "
                       "RETURN "
                       "u.name as name, "
                       "u.id as ID, "
                       "r.date as date, "
                       "r.text as text, "
                       "r.stars as stars,"
                       "r.useful as useful "
                       "ORDER BY Use DESC, date DESC "
                       "LIMIT 10 ".format(id)).data()

    return business, reviews

def get_photo(business, graph):
    # Returns list of all photo_ids for restaurant

    photo_id_list = graph.run(
        "MATCH (b:Business)-[:HAS_PHOTO]->(p:Photo) WHERE b.id = '{}' "
        "RETURN p.id AS id, p.caption AS caption LIMIT toInteger(rand()*3)+1".format(business)).data()

    result = photo_id_list
    return result

def get_city():
    URL = "https://ip8.com/ip"
    page = requests.get(URL)
    data = BeautifulSoup(page.text, 'html.parser')
    ip = str(data)

    reader = geo.Reader("GeoLite2-City.mmdb")
    response = reader.city(ip)

    city = response.city.name
    reader.close()

    return city