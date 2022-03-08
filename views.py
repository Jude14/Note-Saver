from flask import Blueprint,render_template,request,flash, jsonify
from flask.json import jsonify
from flask_login import  login_required, current_user
from .models import Note
from .import db
import json

#this is to setup the blueprint
views = Blueprint('views', __name__) # not necessary to name it as the file 

@views.route('/', methods = ['GET','POST'])
@login_required
def home():
    if request.method== 'POST':
        note = request.form.get('note')

        if len(note)<1:
            flash('Note is too short!',category = 'error')
        else:
            new_note = Note(data=note,user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!',category = 'success')

    return render_template("home.html", user = current_user)# we put user=.. to be able to reference this user
                                                            #in our template and check if its authenticated

@views.route('/delete-note',methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({}) #returning an empty response(empty python disctionary) but we do this cz we need to return something

