# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'App'
        db.create_table(u'error_report_app', (
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('app_id', self.gf('django.db.models.fields.CharField')(max_length=16, primary_key=True)),
        ))
        db.send_create_signal(u'error_report', ['App'])

        # Adding model 'Report'
        db.create_table(u'error_report_report', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['error_report.App'])),
            ('report_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'error_report', ['Report'])


    def backwards(self, orm):
        # Deleting model 'App'
        db.delete_table(u'error_report_app')

        # Deleting model 'Report'
        db.delete_table(u'error_report_report')


    models = {
        u'error_report.app': {
            'Meta': {'object_name': 'App'},
            'app_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'primary_key': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        u'error_report.report': {
            'Meta': {'object_name': 'Report'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['error_report.App']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'report_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['error_report']