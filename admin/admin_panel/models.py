from django.db import models


class User(models.Model):
    id = models.BigIntegerField(primary_key=True)

    class Meta:
        db_table = 'bot_user'


class Phrase(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        db_table = 'bot_phrase'


class OldNewId(models.Model):
    content = models.TextField(primary_key=True, db_column='content')
    class Meta:
        db_table = 'bot_oldnews'