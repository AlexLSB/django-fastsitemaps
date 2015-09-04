# -*- coding: utf-8 -*-
from django.db import models


class SitemapItem(models.Model):
    url = models.URLField(verbose_name=u'url', db_index=True)
    lastmod = models.CharField(verbose_name=u'lastmod', max_length=25)
    changefreq = models.CharField(verbose_name=u'lastmod', max_length=25, default='monthly')
    priority = models.CharField(verbose_name=u'lastmod', max_length=10, default='0.8')

    def as_xml(self, pretty=False):
        if pretty:
            return """<url>\n\
    <loc>%(url)s</loc>\n\
    <lastmod>%(lastmod)s</lastmod>\n\
    <changefreq>%(changefreq)s</changefreq>\n\
    <priority>%(priority)s</priority>\n\
</url>\n""" % {'url': self.url,  'lastmod': self.lastmod, 'changefreq': self.changefreq, 'priority': self.priority}
        else:
            return """<url><loc>%(url)s</loc><lastmod>%(lastmod)s</lastmod><changefreq>%(changefreq)s</changefreq><priority>%(priority)s</priority></url>""" \
                % {'url': self.url,  'lastmod': self.lastmod, 'changefreq': self.changefreq, 'priority': self.priority}


class OldSitemapItem(models.Model):
    url = models.URLField(verbose_name=u'url',  db_index=True)
    lastmod = models.CharField(verbose_name=u'lastmod', max_length=25)
    changefreq = models.CharField(verbose_name=u'lastmod', max_length=25, default='monthly')
    priority = models.CharField(verbose_name=u'lastmod', max_length=10, default='0.8')


class Status(models.Model):
    status = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
