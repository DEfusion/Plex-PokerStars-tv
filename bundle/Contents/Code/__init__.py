# import re, string
# from PMS import *
# from PMS.Objects import *
# from PMS.Shortcuts import *
import htmlentitydefs
import re
from datetime import datetime
from email.utils import parsedate

PLUGIN_TITLE               = 'PokerStars.tv'
PLUGIN_PREFIX              = '/video/pokerstars-tv'

# URLS
BASE_URL                   = 'http://www.pokerstars.tv'
CHANNELS_URL               = '%s/poker-channels' % BASE_URL

# Default artwork and icon(s)
PLUGIN_ARTWORK             = 'art-default.png'
PLUGIN_ICON_DEFAULT        = 'icon-default.png'

###############################################################################
def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, PLUGIN_TITLE, PLUGIN_ICON_DEFAULT, PLUGIN_ARTWORK)
  Plugin.AddViewGroup('Channels', viewMode='InfoList', mediaType='items')
#    Plugin.AddViewGroup("Channels", viewMode="InfoList", mediaType="items")
#    MediaContainer.title1 = L('pokerstars.tv')
#    MediaContainer.art    = R(POKERSTARS_ART)
#    HTTP.CacheTime        = 0 # CACHE_1HOUR

###################################################################################################
# MENUS
###################################################################################################
def MainMenu():
  dir = MediaContainer(viewGroup='Channels')
  channels = HTML.ElementFromURL( CHANNELS_URL, errors='ignore').xpath('//*/div[@id="template"]/ul/li/div[@class="content clearfix"]/a[@class="logo"]')
  for channel in channels:
    url = channel[0].get('href')
    img = channel.xpath('.//img')
    name = img[0].get('alt').replace(' logo', '')
    thumbUrl = img[0].get('src')
    Log( url )
    Log( name )
    Log( thumbUrl ) 
    dir.Append( 
      DirectoryItem( 
        name,
        name,
        thumb=Function(GetThumb, thumbUrl=thumbUrl)
      )
    )
  return dir

###################################################################################################
# HELPERS
###################################################################################################
def GetThumb(thumbUrl):
  data = HTTP.Request(thumbUrl)
  if data:
    return DataObject(data, 'image/png')
  else:
    return Redirect(R(PLUGIN_ICON_DEFAULT))
# @handler('/video/pokerstars-tv', L('pokerstars.tv'))
# def VideoMenu():
#   dir = MediaContainer(viewGroup='Channels')
#   dir.Append(DirectoryItem('foo','bar'))
#   return dir
#     # dir = MediaContainer(mediaType='video', viewGroup='Details')
#     # episodes = JSON.ObjectFromURL(VIMCASTS_FEED_URL)['episodes']
#     # episodes.reverse()  # Newest first
#     # for episode in episodes:
#     #     try:
#     #         url     = episode['quicktime']['url']
#     #         title   = F('episode', episode['episode_number'], episode['title'])
#     #         date    = parsedate(episode['published_at'])
#     #         date    = datetime(*date[:6])
#     #         summary = dehtmlize(episode['abstract'].strip())
#     #         thumb   = episode['poster']
#     #         dir.Append(VideoItem(url, title=title, summary=summary, thumb=thumb,
#     #                              subtitle=date.strftime('%A, %B %e %Y')))
#     #     except AttributeError:
#     #         Log("Something odd with episode, skipping: %s" %
#     #                 episode, debugOnly=False)
#     # return dir

##
# Removes HTML tags from a text string and converts character entities.
# Adapted from:
# http://effbot.org/zone/re-sub.htm#strip-html
#
# @param text The HTML source.
# @return The plain text.  If the HTML source contains non-ASCII
#     entities or character references, this is a Unicode string.
# def dehtmlize(text):
#     def convert_entities(m):
#         text = m.group(0)
#         if text[:2] == "&#":
#             try:
#                 if text[:3] == "&#x":
#                     return unichr(int(text[3:-1], 16))
#                 else:
#                     return unichr(int(text[2:-1]))
#             except ValueError:
#                 pass
#         elif text[:1] == "&":
#             entity = htmlentitydefs.entitydefs.get(text[1:-1])
#             if entity:
#                 if entity[:2] == "&#":
#                     try:
#                         return unichr(int(entity[2:-1]))
#                     except ValueError:
#                         pass
#                 else:
#                     return unicode(entity, "iso-8859-1")
#         return text # leave as is
#     return String.StripTags(re.sub("&#?\w+;", convert_entities, text))

