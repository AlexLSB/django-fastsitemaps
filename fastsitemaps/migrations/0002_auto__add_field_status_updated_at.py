# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Status.updated_at'
        db.add_column(u'fastsitemaps_status', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2015, 9, 4, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Status.updated_at'
        db.delete_column(u'fastsitemaps_status', 'updated_at')


    models = {
        u'fastsitemaps.oldsitemapitem': {
            'Meta': {'object_name': 'OldSitemapItem'},
            'changefreq': ('django.db.models.fields.CharField', [], {'default': "'monthly'", 'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastmod': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'0.8'", 'max_length': '10'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'db_index': 'True'})
        },
        u'fastsitemaps.sitemapitem': {
            'Meta': {'object_name': 'SitemapItem'},
            'changefreq': ('django.db.models.fields.CharField', [], {'default': "'monthly'", 'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastmod': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'0.8'", 'max_length': '10'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'db_index': 'True'})
        },
        u'fastsitemaps.status': {
            'Meta': {'object_name': 'Status'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['fastsitemaps']