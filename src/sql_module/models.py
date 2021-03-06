from peewee import *

class BaseModel(Model):
    class Meta:
        database = MySQLDatabase('money', **{'user': 'root', 'password': '1234', 'host': 'localhost'})


class User(BaseModel):
    class Meta:
        db_table = 'user'


class Category(BaseModel):
    name = TextField()
    type = IntegerField()
    user = ForeignKeyField(db_column='user_id', rel_model=User, to_field='id')

    class Meta:
        db_table = 'category'


class Operation(BaseModel):
    amount = BigIntegerField()
    date = DateField(null=True)
    description = TextField(null=True)
    id_cat = ForeignKeyField(db_column='id_cat', rel_model=Category, to_field='id')
    id_user = ForeignKeyField(db_column='id_user', rel_model=User, to_field='id')

    class Meta:
        db_table = 'operation'
