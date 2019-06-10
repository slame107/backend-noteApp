from pyramid.compat import escape
import re
from docutils.core import publish_parts

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.view import view_config
from backend_noteApp.models.mymodel import Notes

import json
# view config + route (init.py) = end point (pyramid)
@view_config(route_name='add_note', renderer='json')
def add_note(request):
    #next_url = request.route_url('view_notes', pagename='FrontPage')#redirects
    #return {'name':'Root/addNotePage'}
    note = Notes(title='Shawn')
    request.dbsession.add(note) 

@view_config(route_name='view_notes', renderer='json')
def view_notes(request):
    return {'name':'noteView'}
    # pagename = request.matchdict['pagename']

@view_config(route_name='get_note', renderer='json')
def get_note(request):
    notes = request.dbsession.query(Notes).all()
    note_list=[]
    for note in notes:
        # print(note.dict())
        note_list.append(note.dict())
    return dict(success=True, list=note_list)

@view_config(route_name='update_note', renderer='json')
def update_note(request):
    print (request.text) #{"title": "input"}
    post_data = json.loads(request.text) 
    #dbTitle
    title = post_data.get('title')
    note = Notes(title=title)
    #dbNoteContent
    noteContent = post_data.get('noteContent')
    note = Notes(noteContent=noteContent)
    request.dbsession.add(note) 
    return {"Status": "ok"}

@view_config(route_name='delete_note', renderer='json')
def delete_note(request):
    return {'name':'deleteNote'}

@view_config(route_name='get_notelib', renderer='json')
def get_notelib(request):
    return {'name':'getAllNotes'}


