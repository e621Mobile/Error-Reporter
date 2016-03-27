# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

	def forwards(self, orm):
		for i in orm.Report.objects.all():
			i.hash = i.text_hash
			i.save()

	def backwards(self, orm):
		"Write your backwards methods here."

	models = {
		u'error_report.app': {
			'Meta': {'object_name': 'App'},
			'app_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'primary_key': 'True'}),
			'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
		},
		u'error_report.message': {
			'Meta': {'object_name': 'Message'},
			'author': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['error_report.Report']"}),
			'text': ('django.db.models.fields.TextField', [], {}),
			'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
		},
		u'error_report.report': {
			'Meta': {'object_name': 'Report'},
			'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['error_report.App']"}),
			'hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
			'log': ('django.db.models.fields.TextField', [], {'default': "''"}),
			'report_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
			'text': ('django.db.models.fields.TextField', [], {}),
			'text_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '32'}),
			'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 10, 14, 0, 0)'})
		},
		u'error_report.reporttag': {
			'Meta': {'object_name': 'ReportTag'},
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['error_report.Report']"}),
			'tag': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
		}
	}

	complete_apps = ['error_report']
	symmetrical = True
