from app import app
import os
from app.models import site_user, get_restaurant, get_review, suggestion_from_friend
from py2neo import Graph

graph = Graph("bolt://neo4j:group9@localhost:8000")
user = site_user("Pittsburgh", "Pizza")
business, count, res_stars = get_restaurant(graph, user)
print(business['stars'], res_stars)
# user_name, user_id, user_stars = get_review(graph, resid)
# print(user_name, user_stars)
# result = suggestion_from_friend(graph, user_id, user.category)
# print(result)



