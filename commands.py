import sys
from api import app
import json, click
from sqlalchemy import create_engine, MetaData, insert, Table
from sqlalchemy.orm import sessionmaker
from config import Config, BASE_DIR
from api.models.note import NoteModel
from api.models.user import UserModel
from api.models.tag import TagModel
from sqlalchemy.exc import IntegrityError
from flask.cli import AppGroup
import click
import ast


class PythonLiteralOption(click.Option):

    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)


@app.cli.command('createsuperuser')
def create_superuser():
    """
    Creates a user with the admin role
    """
    username = input("Username[default 'admin']:")
    password = input("Password[default 'admin']:")
    user = UserModel(username, password, role="admin")
    user.save()
    print(f"Superuser create successful! id={user.id}")


fixture_cli = AppGroup('fixture')


@fixture_cli.command('load')
@click.option("-fn", "--fixture-name", required=True, type=str, help="data.json")
def load_db(fixture_name, path_to_db=Config.SQLALCHEMY_DATABASE_URI):
    """
    Load fixture data to DB
    """
    path_to_fixture = BASE_DIR / "fixtures" / fixture_name
    engine = create_engine(path_to_db)
    meta = MetaData(bind=engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    with open(path_to_fixture, "r", encoding="UTF-8") as f:
        data = json.load(f)
        nun_records = 0
        for table_name, values in data.items():
            table = Table(table_name, meta, autoload=True)
            query_insert = insert(table)
            for value in values:
                query_insert = query_insert.values(value)
                try:
                    session.execute(query_insert)
                    session.commit()
                    nun_records += 1
                except IntegrityError:
                    print(f"{value}, skipped because it already exists")
    print(f"{nun_records} records added to DB")


@fixture_cli.command('dump')
@click.option("-fn", "--fixture-name", required=True, type=str, help="data.json")
@click.option('--models', type=str, default='', help="UserModel, NoteModel")
def dump_db(models, fixture_name, path_to_db=Config.SQLALCHEMY_DATABASE_URI):
    """
    Dump DB to fixture
    """
    path_to_fixture = BASE_DIR / "fixtures" / fixture_name
    if models:
        models = [getattr(sys.modules[__name__], model_name) for model_name in models.split(', ')]

    engine = create_engine(path_to_db)
    meta = MetaData()
    meta.reflect(bind=engine)
    result = {}
    for table in meta.sorted_tables:
        if models and table.name not in [model.__tablename__ for model in models]:
            continue
        result[table.name] = [dict(row) for row in engine.execute(table.select())]

    with open(path_to_fixture, "w", encoding="UTF-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


app.cli.add_command(fixture_cli)
