from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models.podcast import Podcast

class Note:
    def __init__(self, data):
        self.id = data['id']
        self.reaction = data['reaction']
        self.note = data['note']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.podcast_id = data['podcast_id']

    
    @classmethod
    def make_note(cls, data):

        query  = "INSERT INTO notes(reaction,note,podcast_id) "
        query += "VALUES (%(reaction)s, %(note)s, %(podcast_id)s);"

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_notes_with_podcast(cls, data):
        
        query  = "SELECT * "
        query += "FROM podcasts "
        query += "LEFT JOIN notes ON notes.podcast_id = podcasts.id "
        query += "WHERE podcasts.id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query,data)
        list_of_notes = []
        if len(result) > 0:
            podcast_data = {
                **result[0],
                # "created_at" : result[0]['podcasts.created_at'],
                # "updated_at" : result[0]['podcasts.updated_at'],
                # "id" : result[0]['podcasts.id']
            }

            for row_from_db in result:
                note_in_row = cls(row_from_db)

                note_in_row.podcast = Podcast(podcast_data)
                list_of_notes.append(note_in_row)
            return list_of_notes
        else:
            return []

