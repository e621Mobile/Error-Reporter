# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ReportTag'
        db.create_table(u'error_report_reporttag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['error_report.Report'])),
        ))
        db.send_create_signal(u'error_report', ['ReportTag'])

        # Adding model 'Message'
        db.create_table(u'error_report_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['error_report.Report'])),
        ))
        db.send_create_signal(u'error_report', ['Message'])

        # Deleting field 'Report.text_hash'
        db.delete_column(u'error_report_report', 'text_hash')

        # Adding field 'Report.log'
        db.add_column(u'error_report_report', 'log',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ReportTag'
        db.delete_table(u'error_report_reporttag')

        # Deleting model 'Message'
        db.delete_table(u'error_report_message')

        # Adding field 'Report.text_hash'
        db.add_column(u'error_report_report', 'text_hash',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=32, unique=True),
                      keep_default=False)

        # Deleting field 'Report.log'
        db.delete_column(u'error_report_report', 'log')


    models = {
        u'error_report.app': {
            'Meta': {'object_name': 'App'},
            'app_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'primary_key': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        u'error_report.message': {
            'Meta': {'object_name': 'Message'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['error_report.Report']"})
        },
        u'error_report.report': {
            'Meta': {'object_name': 'Report'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['error_report.App']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'log': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'report_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'error_report.reporttag': {
            'Meta': {'object_name': 'ReportTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['error_report.Report']"}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
        }
    }

    complete_apps = ['error_report']