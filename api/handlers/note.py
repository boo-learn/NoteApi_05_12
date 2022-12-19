from api import app, multi_auth, request, jsonify, db, abort
from api.models.note import NoteModel
from api.models.user import UserModel
from api.models.tag import TagModel
from api.schemas.note import NoteSchema, NoteRequestSchema
from utility.helpers import get_object_or_404
from flask_apispec import doc, marshal_with, use_kwargs
from webargs import fields


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
    # Хорошее решение фильтрации не удаленных заметок: https://blog.miguelgrinberg.com/post/implementing-the-soft-delete-pattern-with-flask-and-sqlalchemy
    if note.deleted:
        abort(404, "Note not found")
    notes = NoteModel.query.join(NoteModel.author).filter((UserModel.id == user.id) | (NoteModel.private == False))
    if note in notes:
        return note, 200
    return "...", 403


@app.route("/notes", methods=["GET"])
@multi_auth.login_required
@doc(summary="Get notes", description='Get notes for current auth User or other public notes', tags=['Notes'])
@marshal_with(NoteSchema(many=True), code=200)
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(security=[{"basicAuth": []}])
def get_notes():
    user = multi_auth.current_user()
    notes = NoteModel.query.join(NoteModel.author).filter(NoteModel.deleted == False).filter(
        (UserModel.id == user.id) | (NoteModel.private == False))
    return notes, 200


@app.route("/notes", methods=["POST"])
@multi_auth.login_required
@doc(summary="Create new note", description='Create new note for current auth User', tags=['Notes'])
@marshal_with(NoteSchema, code=201)
@use_kwargs(NoteRequestSchema, location='json')
# @use_kwargs({"text": fields.Str(required=True), "private": fields.Boolean()})
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(security=[{"basicAuth": []}])
def create_note(**kwargs):
    user = multi_auth.current_user()
    note = NoteModel(author_id=user.id, **kwargs)
    note.save()
    return note, 201


@app.route("/notes/<int:note_id>", methods=["PUT"])
@marshal_with(NoteSchema, code=200)
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
    return note, 200


@app.route("/notes/<int:note_id>", methods=["DELETE"])
@doc(summary="Delete note", tags=['Notes'])
@multi_auth.login_required
@doc(security=[{"basicAuth": []}])
def delete_note(note_id):
    # TODO: Пользователь может удалять ТОЛЬКО свои заметки.
    #  Попытка удалить чужую заметку, возвращает ответ с кодом 403
    note = get_object_or_404(NoteModel, note_id)
    note.delete()
    return '', 204


@app.route("/notes/<int:note_id>/tags", methods=["PUT"])
@doc(summary="Set tags to Note", tags=['Notes'])
@use_kwargs({"tags_id": fields.List(fields.Int())}, location=('json'))
@marshal_with(NoteSchema)
def note_add_tags(note_id, **kwargs):
    note = get_object_or_404(NoteModel, note_id)
    tags_id = kwargs["tags_id"]
    for tag_id in tags_id:
        tag = get_object_or_404(TagModel, tag_id)
        note.tags.append(tag)

    db.session.commit()
    return note, 200


@app.route('/notes/<int:note_id>/importance', methods=["PUT"])
@marshal_with(NoteSchema, 200)
@doc(summary="Change importance", tags=['Notes'])
def change_importance(note_id):
    note = get_object_or_404(NoteModel, note_id)
    note.importance %= 3
    note.importance += 1
    note.save()

    return note, 200
