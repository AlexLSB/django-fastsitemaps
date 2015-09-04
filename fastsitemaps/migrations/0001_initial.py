# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SitemapItem'
        db.create_table(u'fastsitemaps_sitemapitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, db_index=True)),
            ('lastmod', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('changefreq', self.gf('django.db.models.fields.CharField')(default='monthly', max_length=25)),
            ('priority', self.gf('django.db.models.fields.CharField')(default='0.8', max_length=10)),
        ))
        db.send_create_signal(u'fastsitemaps', ['SitemapItem'])

        # Adding model 'OldSitemapItem'
        db.create_table(u'fastsitemaps_oldsitemapitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, db_index=True)),
            ('lastmod', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('changefreq', self.gf('django.db.models.fields.CharField')(default='monthly', max_length=25)),
            ('priority', self.gf('django.db.models.fields.CharField')(default='0.8', max_length=10)),
        ))
        db.send_create_signal(u'fastsitemaps', ['OldSitemapItem'])

        # Adding model 'Status'
        db.create_table(u'fastsitemaps_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'fastsitemaps', ['Status'])


    def backwards(self, orm):
        # Deleting model 'SitemapItem'
        db.delete_table(u'fastsitemaps_sitemapitem')

        # Deleting model 'OldSitemapItem'
        db.delete_table(u'fastsitemaps_oldsitemapitem')

        # Deleting model 'Status'
        db.delete_table(u'fastsitemaps_status')


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
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['fastsitemaps']