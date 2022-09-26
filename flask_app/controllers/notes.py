from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.note import Note



@app.route('/note/<int:id>')
def podcast_notes(id):
    session['podcast_id'] = id
    podcast_data = {
        "id" : id
    }
    return render_template('notes.html', list_of_notes=Note.get_all_notes_with_podcast(podcast_data))

@app.route('/create/note', methods=['POST'])
def create_note():
    note_data = {
        "reaction" : request.form['reaction'],
        "note" : request.form["note"],
        "podcast_id" : session['podcast_id']
    }
    Note.make_note(note_data)

    podcast_id = session['podcast_id']
    return redirect(f'/note/{podcast_id}')