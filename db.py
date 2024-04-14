from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
#
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
#a connector or a bridge tha connects flask and database