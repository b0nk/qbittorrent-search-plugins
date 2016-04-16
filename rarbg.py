#VERSION: 1.00
#AUTHORS: b0nk

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the author nor the names of its contributors may be
#      used to endorse or promote products derived from this software without
#      specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from novaprinter import prettyPrinter
from helpers import retrieve_url, download_file
import urllib
import json


class rarbg(object):
    url = 'https://rarbg.to'
    name = 'rarbg (torrentApi)'

    supported_categories = {'all': ''}

    def __init__(self):
        pass

    def search(self, what, cat='all'):
        # Get token
        baseURL = "https://torrentapi.org/pubapi_v2.php?%s"
        params = urllib.urlencode({'get_token': 'get_token'})
        response = retrieve_url(baseURL % params)
        j = json.loads(response)
        token = j['token']

        # get JSON

        what = urllib.unquote(what)
        params = urllib.urlencode({'mode': 'search', 'search_string': what, 'ranked': 0, 'limit': 100, 'sort': 'seeders', 'format': 'json_extended', 'token': token})

        response = retrieve_url(baseURL % params)
        j = json.loads(response)

        for i in j['torrent_results']:

            tbytes = float(i['size'])
            size = "-1"

            if tbytes > 1024 * 1024 * 1024:
                size = "%.1f GB" % (tbytes / (1024 * 1024 * 1024))

            elif tbytes > 1024 * 1024:
                size = "%.1f MB" % (tbytes / (1024 * 1024))

            elif tbytes > 1024:
                size = "%.1f KB" % (tbytes / 1024)

            else:
                size = "%.1f B" % (tbytes)

            res = dict(link=i['download'],
                       name=i['title'],
                       size=size,
                       seeds=i['seeders'],
                       leech=i['leechers'],
                       engine_url=self.url,
                       desc_link=i['info_page'])

            prettyPrinter(res)
