#-*- coding: utf-8 -*-
__author__ = 'muti'
__copyright__ = 'npcomms'

import ast
import urllib, urllib2
import json
import time

def get_video_info(source):
    """

    :param source: string
    :return: json
    """

    sp_source = source.split(';')
    if len(sp_source) == 2:
        source_info = [
            { "src": sp_source[0], "default": True, "label": '720p', "is_hd": True },
            { "src": sp_source[1], "default": True, "label": '480', "is_hd": False }
        ]
    elif len(sp_source) == 1:
        source_info = [
            { "src": source, "default": True, "label": '720p', "is_hd": True }
        ]
    else:
        source_info = []

    return source_info
    #return json.dumps(source_info)


def get_caption_info(caption_info):
    """

    :param caption_info:
    :return:
    """

    if caption_info:

        response = urllib2.urlopen(caption_info)
        #caption_data = json.load(response)
        caption_data = response

    else:
        #caption_data = json.dumps([])
        caption_data = []

    return caption_data

def get_player_info(lang='ko', preload='auto', controls=True, width='100%', height='400', speed=[0.5,1,1.5,2]):
    """

    :param lang:
    :param preload:
    :param controls:
    :param width:
    :param height:
    :param speed:
    :return:
    """

    player_info = {
        "language": lang,
        "preload": preload,
        'controls': controls,
        "width": width,
        "height": height,
        "playbackRates": speed,
    }

    return player_info
    #return json.dumps(player_info)

def get_id():
    current_milli_time = int(round(time.time() * 1000))
    # print (current_milli_time)
    return 'zplay' + str(current_milli_time)


if __name__ == "__main__":
    print get_id()