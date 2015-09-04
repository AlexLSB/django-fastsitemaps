# coding: utf-8

from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site
from django.conf import settings
from django.db import connection, transaction
import os
import gc
from shutil import move
from .models import *


class RequestSitemap(Sitemap):
    def __init__(self, request=None):
        self.request = request

    def __get(self, name, obj, default=None):
        try:
            attr = getattr(self, name)
        except AttributeError:
            return default
        if callable(attr):
            return attr(obj)
        return attr

    def get_site(self, site):
        if site is None:
            if Site._meta.installed:
                try:
                    site = Site.objects.get_current()
                except Site.DoesNotExist:
                    pass
            if site is None:
                raise ImproperlyConfigured("In order to use Sitemaps you must either use the sites framework or pass in a Site or RequestSite object in your view code.")
        return site

    def get_urls(self, page=1, site=None):
        "Returns a generator instead of a list, also prevents http: doubling up"
        site = self.get_site(site)
        for item in self.paginator.page(page).object_list:
            loc = self.__get('location', item)
            if not loc.startswith('http'):
                loc = "http://%s%s" % (site.domain, loc)
            priority = self.__get('priority', item, None)
            url_info = {
                'item':       item,
                'location':   loc,
                'lastmod':    self.__get('lastmod', item, None),
                'changefreq': self.__get('changefreq', item, None),
                'priority':   str(priority is not None and priority or ''),
            }
            yield url_info


class FileSitemap(RequestSitemap):

    def get_info(self, location, lastmod, changefreq, priority,  site=None):
        site = self.get_site(site)
        if not location.startswith('http'):
                location = "http://%s%s" % (site.domain, location)
        return {
            'url':   location,
            'lastmod':    lastmod.strftime('%Y-%m-%d'),
            'changefreq': changefreq,
            'priority':   str(priority is not None and priority or '')}


def prepare_db():
    cursor = connection.cursor()
    cursor.execute('''TRUNCATE TABLE fastsitemaps_oldsitemapitem;
        INSERT INTO fastsitemaps_oldsitemapitem
SELECT *
FROM fastsitemaps_sitemapitem;
    TRUNCATE TABLE fastsitemaps_sitemapitem;''')


def get_diff():
    cursor = connection.cursor()
    cursor.execute('''SELECT A.url
FROM `fastsitemaps_oldsitemapitem` as A
    LEFT JOIN `fastsitemaps_sitemapitem` as B ON (A.url = B.url)
WHERE B.url IS NULL;''')
    return cursor.fetchall()


def get_diff_cnt():
    cursor = connection.cursor()
    cursor.execute('''SELECT count(A.url)
FROM `fastsitemaps_oldsitemapitem` as A
    LEFT JOIN `fastsitemaps_sitemapitem` as B ON (A.url = B.url)
WHERE B.url IS NULL;''')
    return cursor.fetchone()[0]


def write_to_file(location, lastmod, site=None):
    self.out_file.write("""<url>\n\
<loc>%(loc)s</loc>\n\
<lastmod>%(lastmod)s</lastmod>\n\
<changefreq>%(changefreq)s</changefreq>\n\
<priority>%(priority)s</priority>\n\
</url>\n""" % self.get_info(location, lastmod, site))
    return True


def db_sitemap_to_file(filename):
    '''
        Save all urls from SitemapItem table to file specified with filename
    '''
    tempfilename = os.path.join(settings.MEDIA_ROOT, 'temp_sitemap.xml')
    with open(tempfilename, 'w') as sitemap_file:
        sitemap_file.write('''<?xml version="1.0" encoding="utf8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">''')
        for item in SitemapItem.objects.all().iterator():
            sitemap_file.write(item.as_xml())
        sitemap_file.write('''</urlset>''')
    return move(tempfilename, filename)


@transaction.commit_on_success
def quick_db_file_sitemap_generator(request, sitemaps, filename):
    stmp_cnt = 0
    stmp_len = len(sitemaps)
    for key, SitemapClass in sitemaps.iteritems():
        sitemap = SitemapClass()
        transcounter = 0
        stmp_cnt += 1
        set_status('%s (%d/%d)' % (key, stmp_cnt, stmp_len))
        print key
        for item in sitemap.items_iterator():
            sm_item = SitemapItem(**item)
            sm_item.save()
            transcounter += 1
            if (transcounter == 1000):
                transaction.commit()
                transcounter = 0
        gc.collect()
    return db_sitemap_to_file(filename)


def db_file_sitemap_generator(request, sitemaps, filename):
    if settings.DEBUG:
        return slow_db_file_sitemap_generator(request, sitemaps, filename)
    else:
        return quick_db_file_sitemap_generator(request, sitemaps, filename)


def to_xml(item):
    return """<url>\n\
    <loc>%(url)s</loc>\n\
    <lastmod>%(lastmod)s</lastmod>\n\
    <changefreq>%(changefreq)s</changefreq>\n\
    <priority>%(priority)s</priority>\n\
</url>\n""" % {'url': item['url'],  'lastmod': item['lastmod'], 'changefreq': item['changefreq'], 'priority': item['priority']}


def slow_db_file_sitemap_generator(request, sitemaps, filename):
    stmp_cnt = 0
    stmp_len = len(sitemaps)
    tempfilename = os.path.join(settings.MEDIA_ROOT, 'temp_sitemap.xml')
    with open(tempfilename, 'w') as sitemap_file:
        sitemap_file.write('''<?xml version="1.0" encoding="utf8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">''')
        for key, SitemapClass in sitemaps.iteritems():
            sitemap = SitemapClass()
            stmp_cnt += 1
            set_status('%s (%d/%d)' % (key, stmp_cnt, stmp_len))
            print key
            for item in sitemap.items_iterator():
                sitemap_file.write(to_xml(item))
            gc.collect()
        sitemap_file.write('''</urlset>''')
    """  add from file to db not yet working good
    r = re.compile(r'<loc>(?P<url>.*?)</loc>[^<]+<lastmod>(?P<lastmod>.*?)</lastmod>[^<]+<changefreq>(?P<changefreq>.*?)</changefreq>[^<]+<priority>(?P<priority>.*?)</priority>',  re.DOTALL)
    with open(filename, 'r') as f:
        objs = []
        for i in r.finditer(f.read()):
            i = i.groupdict()
            objs.append(SitemapItem(
                url=i['url'],
                lastmod=i['lastmod'],
                changefreq=i['changefreq'],
                priority=i['priority'],))
        sitemap = SitemapItem.objects.bulk_create(objs)
    """
    return move(tempfilename, filename)


def set_status(status_text):
    ss = Status.objects.all()
    if ss.count() > 0:
        s = Status.objects.first()
        s.status = status_text
        s.save()
    else:
        s = Status.objects.create(status="Запущено обновление sitemap.xml ...")


def generate_sitemap_to_file(request, sitemaps, filename):
    set_status("Запущено обновление sitemap.xml ...")
    prepare_db()
    db_file_sitemap_generator(request, sitemaps, filename)
    diff = get_diff()
    set_status('Обновление sitemap.xml завершено.')
    return diff
