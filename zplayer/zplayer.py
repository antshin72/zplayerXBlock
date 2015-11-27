#-*- coding: utf-8 -*-
__author__ = 'muti'
__copyright__ = 'npcomms'

""" videojsXBlock main Python class"""

import pkg_resources
from django.template import Context, Template

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean
from xblock.fragment import Fragment

import params

class ZplayerXBlock(XBlock):

    '''
    Icon of the XBlock. Values : [other (default), video, problem]
    '''
    icon_class = "video"

    '''
    Fields
    '''
    display_name = String(display_name="Display Name",
        default="zplayerXBlock(kmooc)",
        scope=Scope.settings,
        help="This name appears in the horizontal navigation at the top of the page.")

    url = String(display_name="Video URL",
        default="http://vjs.zencdn.net/v/oceans.mp4",
        scope=Scope.content,
        help="The URL for your video.")

    allow_download = Boolean(display_name="Video Download Allowed",
        default=False,
        scope=Scope.content,
        help="Allow students to download this video.")

    source_text = String(display_name="Source document button text",
        default="",
        scope=Scope.content,
        help="Add a download link for the source file of your video. Use it for example to provide the PowerPoint or PDF file used for this video.")

    source_url = String(display_name="Source document URL",
        default="",
        scope=Scope.content,
        help="Add a download link for the source file of your video. Use it for example to provide the PowerPoint or PDF file used for this video.")

    start_time = String(display_name="Start time",
        default="",
        scope=Scope.content,
        help="The start and end time of your video. Equivalent to 'video.mp4#t=startTime,endTime' in the url.")

    end_time = String(display_name="End time",
        default="",
        scope=Scope.content,
        help="The start and end time of your video. Equivalent to 'video.mp4#t=startTime,endTime' in the url.")

    """ zplayer script define """
    video_id = String(display_name="videoplayer dom ID", default="zplayer", scope=Scope.content, help="set Node")
    video_lang = String(display_name="콘트롤러 언어셋", default="ko", scope=Scope.content, help="언어셋 설정을 정의합니다.(기본값: ko [ar,bg,ca,cs,de,es,fr,hu,it,ja,ko,nl,pt-BR,ru,tr,uk,vl,zh-CN,zh-TW])")
    preload = String(display_name="프리로드 처리", default="auto", scope=Scope.content, help="프리로드 처리 설정(기본값 auto)")
    video_width = Integer(display_name="동영상 가로해상도", default=540, scope=Scope.content, help="동영상의 가로해상도를 설정합니다.(기본값: 540)")
    video_height = Integer(display_name="동영상 세로해상도", default=304, scope=Scope.content, help="동영상의 가로해상도를 설정합니다.(기본값: 304)")
    video_poster = String(display_name="thumbnail url", default="http://119.205.215.21/Upload/20140924195416.jpg", scope=Scope.content, help="")
    video_title = String(display_name="video title", default="kmoocs video title", scope=Scope.content, help="비디오에 대한 제목을 설정합니다")

    source_url = String(display_name="영상스트리밍 URL", default="http://vjs.zencdn.net/v/oceans.mp4", scope=Scope.content, help="영상 스트리밍 주소를 설정합니다")
    caption_info = String(display_name="자막 정보 URL", default="", scope=Scope.content, help="json형태로 구성된 자막의 정보 취득 URL을 설정합니다")


    '''
    Util functions
    '''
    def load_resource(self, resource_path):
        """
        Gets the content of a resource
        """
        resource_content = pkg_resources.resource_string(__name__, resource_path)

        return unicode(resource_content)

    def render_template(self, template_path, context={}):
        """
        Evaluate a template by resource path, applying the provided context
        """
        template_str = self.load_resource(template_path)
        return Template(template_str).render(Context(context))

    '''
    Main functions
    '''
    def student_view(self, context=None):
        """
        The primary view of the XBlock, shown to students
        when viewing courses.
        """


        source_list = params.get_video_info(self.source_url)
        caption_list = params.get_caption_info(self.caption_info)

        player_info = params.get_player_info(lang=self.video_lang, preload=self.preload, width=self.video_width, height=self.video_height)


        fullUrl = self.url
        if self.start_time != "" and self.end_time != "":
            fullUrl += "#t=" + self.start_time + "," + self.end_time
        elif self.start_time != "":
            fullUrl += "#t=" + self.start_time
        elif self.end_time != "":
            fullUrl += "#t=0," + self.end_time

        context = {
            'video_id': self.video_id,
            'allow_download': self.allow_download,
            'source_text': self.source_text,
            'source_list': source_list,
            'caption_info': caption_list,
            'video_title': self.video_title,
            'video_poster': self.video_poster,
            'video_lang': self.video_lang,
            'preload': self.preload,
            'video_width': self.video_width,
            'video_height': self.video_height,
            'video_poster': self.video_poster,
            'video_title': self.video_title,
        }
        html = self.render_template('static/html/zplayer_view.html', context)

        frag = Fragment(html)
        # frag.add_css(self.load_resource("static/css/video-js.min.css"))
        # frag.add_css(self.load_resource("static/css/videojs.css"))
        frag.add_css(self.load_resource("static/css/zplayer.css"))
        # frag.add_javascript(self.load_resource("static/js/video-js.js"))
        # frag.add_javascript(self.load_resource("static/js/videojs_view.js"))
        frag.add_javascript(self.load_resource("static/js/zplayer.js"))
        frag.add_javascript(self.load_resource("static/js/lang/ko.js"))
        frag.add_javascript(self.load_resource("static/js/zplayer_view.js"))

        frag.initialize_js('zplayerXBlockInitView')

        """
        todo frag.initialize_js 의 파라미터 처리 확인하여 연동 해야 함.
        frag.initialize_js('initContent', {'id_name': self.video_id, 'player_info': player_info,
                                           'source_info': source_list, 'video_title': self.video_title,
                                           'video_poster': self.video_poster, 'caption_info': caption_list})
        """




        return frag

    def studio_view(self, context=None):
        """
        The secondary view of the XBlock, shown to teachers
        when editing the XBlock.
        """
        context = {
            'display_name': self.display_name,
            'url': self.url,
            'allow_download': self.allow_download,
            'source_text': self.source_text,
            'source_url': self.source_url,
            'start_time': self.start_time,
            'end_time': self.end_time,

            'video_lang': self.video_lang,
            'preload': self.preload,
            'video_width': self.video_width,
            'video_height': self.video_height,
        }
        html = self.render_template('static/html/zplayer_edit.html', context)

        frag = Fragment(html)
        frag.add_javascript(self.load_resource("static/js/videojs_edit.js"))
        frag.initialize_js('zplayerXBlockInitStudio')
        return frag

    @XBlock.json_handler
    def save_videojs(self, data, suffix=''):
        """
        The saving handler.
        """
        self.display_name = data['display_name']
        self.url = data['url']
        self.allow_download = True if data['allow_download'] == "True" else False # Str to Bool translation
        self.source_text = data['source_text']
        self.source_url = data['source_url']
        self.start_time = ''.join(data['start_time'].split()) # Remove whitespace
        self.end_time = ''.join(data['end_time'].split()) # Remove whitespace

        return {
            'result': 'success',
        }

    """
    zplayer를 xblock에 적용할때만 사용한다
    """
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("zplayerXblock",
            """\
                <vertical_demo>
                    <zplayer href="https://vimeo.com/46100581" maxwidth="800" />
                    <html_demo><div>Rate the video:</div></html_demo>
                    <thumbs />
                </vertical_demo>
             """)
        ]