# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'E621Webm.image'
        db.add_column(u'e621_webm_e621webm', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'E621Webm.image'
        db.delete_column(u'e621_webm_e621webm', 'image')


    models = {
        u'e621_webm.e621webm': {
            'Meta': {'object_name': 'E621Webm'},
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'post_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['e621_webm']