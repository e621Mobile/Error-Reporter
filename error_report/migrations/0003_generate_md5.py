# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

import hashlib

class Migration(DataMigration):

	def forwards(self, orm):
		del_rep = [];
		hashes = [];
		
		for i in orm.Report.objects.order_by("report_id").all():
			h = hashlib.md5(i.text).hexdigest();
			
			if(h in hashes):
				del_rep.append(i.report_id);
			else:
				hashes.append(h);
				i.save();
		
		orm.Report.objects.filter(report_id__in=del_rep).delete()

	def backwards(self, orm):
		"Write your backwards methods here."

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
			'text': ('django.db.models.fields.TextField', [], {}),
			'text_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'})
		}
	}

	complete_apps = ['error_report']
	symmetrical = True
