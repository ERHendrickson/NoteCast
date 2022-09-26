from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE


class Podcast:
    def __init__(self, data):
        self.id = data['id']
        self.img = data['img']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_podcast(data):
        is_valid = True
        if data['podcast_name'] == "":
            flash("Please input the name of the podcast or I no worky", "error_search_podcast")
            is_valid = False
        return is_valid

    @classmethod
    def save_podcast(cls, data):
        query  = "INSERT INTO podcasts(img, description) "
        query += "VALUES (%(img)s, %(description)s);"

        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_all_podcasts(cls):
        query  = "SELECT * "
        query += "FROM podcasts;"

        results = connectToMySQL(DATABASE).query_db(query)
        list_of_podcasts = []

        for row in results:
            podcast_in_row = cls(row)
            list_of_podcasts.append(podcast_in_row)
        return list_of_podcasts

        