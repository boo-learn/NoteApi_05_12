from api import app, multi_auth, request, jsonify, db
from api.models.note import NoteModel
from api.models.tag import TagModel
from api.schemas.tag import TagSchema, TagRequestSchema
from utility.helpers import get_object_or_404
from flask_apispec import doc, marshal_with, use_kwargs
from sqlalchemy.exc import IntegrityError


@app.route("/tags", methods=["GET"])
@doc(summary='Get all tags', tags=['Tags'])
@marshal_with(TagSchema(many=True), code=200)
def get_tags():
    tags = TagModel.query.all()
    return tags, 200


@app.route("/users/<int:tag_id>", methods=["GET"])
@doc(summary='Get tag by id', tags=['Tags'])
@marshal_with(TagSchema, code=200)
def get_tag_by_id(tag_id):
    tag = get_object_or_404(TagModel, tag_id)
    return tag, 200


@app.route("/tags", methods=["POST"])
@doc(summary='Create new tag', tags=['Tags'])
@marshal_with(TagSchema, code=201)
@use_kwargs(TagRequestSchema, location='json')
def create_tag(**kwargs):
    tag = TagModel(**kwargs)
    try:
        tag.save()
    except IntegrityError:
        db.session.rollback()
        return "tag name must be unique", 400
    return tag, 201


@app.route("/users/<int:tag_id>", methods=["PUT"])
@doc(summary='Edit tag', tags=['Tags'])
def edit_tag(tag_id):
    raise NotImplemented("Метод не реализован")


@app.route("/users/<int:tag_id>", methods=["DELETE"])
@doc(summary='Delete tag', tags=['Tags'])
def delete_tag(tag_id):
    raise NotImplemented("Метод не реализован")
