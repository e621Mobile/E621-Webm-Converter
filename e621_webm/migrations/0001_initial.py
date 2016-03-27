# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'E621Webm'
        db.create_table(u'e621_webm_e621webm', (
            ('post_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True)),
        ))
        db.send_create_signal(u'e621_webm', ['E621Webm'])


    def backwards(self, orm):
        # Deleting model 'E621Webm'
        db.delete_table(u'e621_webm_e621webm')


    models = {
        u'e621_webm.e621webm': {
            'Meta': {'object_name': 'E621Webm'},
            'post_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['e621_webm']