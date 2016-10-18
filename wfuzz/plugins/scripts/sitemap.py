from wfuzz.plugin_api.mixins import DiscoveryPluginMixin
from wfuzz.plugin_api.base import BasePlugin
from wfuzz.plugin_api.urlutils import parse_url
from wfuzz.exception import FuzzException
from wfuzz.externals.moduleman.plugin import moduleman_plugin

import xml.dom.minidom
import urlparse

@moduleman_plugin
class sitemap(BasePlugin, DiscoveryPluginMixin):
    name = "sitemap"
    author = ("Xavi Mendez (@xmendez)",)
    version = "0.1"
    summary = "Parses sitemap.xml file. Optional: discovery.bl=\".txt,.gif\""
    category = ["default", "active", "discovery"]
    priority = 99

    def validate(self, fuzzresult):
	return fuzzresult.history.urlparse.file_fullname == "sitemap.xml" and fuzzresult.code == 200

    def process(self, fuzzresult):
	base_url = fuzzresult.url

	try:
	    dom = xml.dom.minidom.parseString(fuzzresult.history.content)
	except:
	    raise FuzzException(FuzzException.FATAL, 'Error while parsing %s.' % fuzzresult.url)

	urlList = dom.getElementsByTagName("loc")
	for url in urlList:
	    u = url.childNodes[0].data

	    if fuzzresult.history.urlparse.domain == parse_url(u).domain:
		self.queue_url(u)

