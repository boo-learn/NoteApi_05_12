from api import app, docs, db
from config import Config
from api.models.note import NoteModel
from api.models.user import UserModel
from api.models.tag import TagModel
from api.handlers import auth, note, user, tag, file
import commands


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'NoteModel': NoteModel, 'UserModel': UserModel, 'TagModel': TagModel}


# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE

# USERS
docs.register(user.get_user_by_id)
docs.register(user.get_users)
docs.register(user.create_user)

# NOTES!
docs.register(note.get_note_by_id)
docs.register(note.get_notes)
docs.register(note.create_note)
docs.register(note.note_add_tags)

# TAGS
docs.register(tag.get_tag_by_id)
docs.register(tag.get_tags)
docs.register(tag.create_tag)
docs.register(tag.edit_tag)
docs.register(tag.delete_tag)

# FILES
docs.register(file.upload_file)
docs.register(file.download_file)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
