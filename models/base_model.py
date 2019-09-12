import os
import peewee as pw
import datetime
from database import db


class BaseModel(pw.Model):
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    updated_at = pw.DateTimeField(default=datetime.datetime.now)

    errors = None

    def save(self, *args, **kwargs):
        self.errors = self.errors or []
        self.validate()

        if len(self.errors) == 0:
            self.updated_at = datetime.datetime.now()
            return super(BaseModel, self).save(*args, **kwargs)
        else:
            return 0

    def validate(self):
        print(
            f"Warning validation method not implemented for {str(type(self))}")
        return True

    class Meta:
        database = db
        legacy_table_names = False

class IntArrayField(pw.Field):
	db_field = 'integer[3]'
	def db_value(self, value):
		return value

	def python_value(self, value):
		return value