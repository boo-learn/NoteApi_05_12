from api import ma
from api.models.note import NoteModel
from api.schemas.user import UserSchema
from api.schemas.tag import TagSchema


#       schema        flask-restful
# object ------>  dict ----------> json

class NoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = NoteModel

    id = ma.auto_field()
    text = ma.auto_field()
    private = ma.auto_field()
    author = ma.Nested(UserSchema())
    deleted = ma.auto_field()
    importance = ma.auto_field()
    tags = ma.Nested(TagSchema(many=True))


# Десериализация запроса(request)
class NoteRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = NoteModel

    text = ma.Str()
    private = ma.Boolean()


note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
