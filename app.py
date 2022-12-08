from api import app, docs
from config import Config
from api.handlers import auth, note, user

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE
docs.register(user.get_user_by_id)
docs.register(user.get_users)
docs.register(user.create_user)
if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
