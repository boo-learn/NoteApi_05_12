from api import app, multi_auth, request, jsonify
from api.models.note import NoteModel
from api.models.user import UserModel
from api.schemas.note import note_schema, notes_schema, NoteSchema
from utility.helpers import get_object_or_404
from flask_apispec import doc, marshal_with, use_kwargs


@app.route("/notes/<int:note_id>", methods=["GET"])
@multi_auth.login_required
@doc(summary="Get note by id", description='Get note by id for current auth User or other public note', tags=['Notes'])
@marshal_with(NoteSchema, code=200)
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(responses={"404": {"description": "Not found"}})
@doc(responses={"403": {"description": "Forbidden"}})
@doc(security=[{"basicAuth": []}])
def get_note_by_id(note_id):
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    notes = NoteModel.query.join(NoteModel.author).filter((UserModel.id == user.id) | (NoteModel.private == False))
    if note in notes:
        return note, 200
    return "...", 403


@app.route("/notes", methods=["GET"])
@multi_auth.login_required
def get_notes():
    # TODO: авторизованный пользователь получает только свои заметки и публичные заметки других пользователей
    user = multi_auth.current_user()
    notes = NoteModel.query.all()
    return jsonify(notes_schema.dump(notes)), 200


@app.route("/notes", methods=["POST"])
@multi_auth.login_required
def create_note():
    user = multi_auth.current_user()
    note_data = request.json
    note = NoteModel(author_id=user.id, **note_data)
    note.save()
    return note_schema.dump(note), 201


@app.route("/notes/<int:note_id>", methods=["PUT"])
@multi_auth.login_required
def edit_note(note_id):
    # TODO: Пользователь может редактировать ТОЛЬКО свои заметки.
    #  Попытка редактировать чужую заметку, возвращает ответ с кодом 403
    author = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    note_data = request.json
    note.text = note_data["text"]
    note.private = note_data.get("private") or note.private
    note.save()
    return note_schema.dump(note), 200


@app.route("/notes/<int:note_id>", methods=["DELETE"])
@multi_auth.login_required
def delete_note(self, note_id):
    # TODO: Пользователь может удалять ТОЛЬКО свои заметки.
    #  Попытка удалить чужую заметку, возвращает ответ с кодом 403
    raise NotImplemented("Метод не реализован")
