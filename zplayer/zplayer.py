#-*- coding: utf-8 -*-
__author__ = 'muti'
__copyright__ = 'npcomms'

""" videojsXBlock main Python class"""

import os, time

import pkg_resources
from django.template import Context, Template

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean, List
from xblock.fragment import Fragment



## todo view, headers를참조하여 트래킹로그json구성할


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
        default="kmoocs Extend Video Player",
        scope=Scope.settings,
        help="비디오 제목을 설정합니다.")

    allow_download = Boolean(display_name="비디오영상 다운로드 허용여부",
        default=False,
        scope=Scope.content,
        help="수강자가 비디오 영상 원본을 다운로드 허용할지를 설정합니다.")

    allow_caption_download = Boolean(display_name="자막파일 다운로드 허용여부",
        default=False,
        scope=Scope.content,
        help="수강자가 자막파일을 다운로드 허용할지를 설정합니다.")
    video_poster = String(display_name="thumbnail url", default="", scope=Scope.content, help="동영상의 썸네일 경로를 설정합니다.")

    source_url = String(display_name="영상스트리밍 URL",
                        default="http://vod.kmooc.kr/vod/2015/09/30/6098c795-39a8-5ec5-9683-49f12ba48dfd.mp4",
                        scope=Scope.content, help="영상 스트리밍 주소를 설정합니다.")
    caption_info = List(display_name="자막 정보 URL", default="", scope=Scope.content, help="json형태로 구성된 자막의 정보 취득 URL을 설정합니다.")

    """ zplayer script define """


    video_id = String(display_name="videoplayer dom ID", default=params.get_id(), scope=Scope.content, help="set Node")
    video_lang = String(display_name="콘트롤러 언어셋", default="ko", scope=Scope.content, help="언어셋 설정을 정의합니다.(기본값: ko [ar,bg,ca,cs,de,es,fr,hu,it,ja,ko,nl,pt-BR,ru,tr,uk,vl,zh-CN,zh-TW])")
    preload = String(display_name="프리로드 처리", default="auto", scope=Scope.content, help="프리로드 처리 설정(기본값 auto)")
    video_width = Integer(display_name="동영상 가로해상도", default=800, scope=Scope.content, help="동영상의 가로해상도를 설정합니다.(기본값: 540)")
    video_height = Integer(display_name="동영상 세로해상도", default=450, scope=Scope.content, help="동영상의 가로해상도를 설정합니다.(기본값: 304)")

    studio_modify = Boolean(display_name="스튜디오 편집모드", default=False, scope=Scope.content, help="스튜디오 저작 처리인지 여부판단 파라미터")


    #tracking 관련 정보 파라미터
    tracking_url = String(display_name="tracking url", default="http://mme.kmooc.kr/logging", scope=Scope.content, help="트래킹 수집 URL을 입력한다")
    onplay_callback = Integer(display_name="callback second set", default=3, scope=Scope.content, help="트래킹 반복 주기초를 기록")
    org_id = String(display_name="기관ID", default="edX", scope=Scope.content, help="get Org ID")
    # use_caption_list = String(display_name="저장된 캡션목록", default="", scope=Scope.content, help="saved caption language key")
    # user_id = String(display_name="SESSION ID", default="", scope=Scope.content, help="get Session ID")


    '''
    Util functions
    '''
    def load_resource(self, resource_path):
        """
        Gets the content of a resource
        """
        resource_content = pkg_resources.resource_string(__name__, resource_path)

        return unicode(resource_content, 'utf-8')

    def render_template(self, template_path, context={}):
        """
        Evaluate a template by resource path, applying the provided context
        """
        template_str = self.load_resource(template_path)
        return Template(template_str).render(Context(context))


    def get_resource_string(self, path):
        path = os.path.join('public', path)
        resource_string = pkg_resources.resource_string(__name__, path)
        return resource_string.decode('utf-8')

    def get_resource_url(self, path):
        path = os.path.join('public', path)
        resource_url = self.runtime.local_resource_url(self, path)
        return resource_url
    '''
    Main functions
    '''
    def student_view(self, request, context=None):

        #### Edx Info ####

        #### Edx Info End ####

        source_list = params.get_video_info(self.source_url)

        player_info = params.get_player_info(
            lang=self.video_lang, preload=self.preload, width=self.video_width, height=self.video_height,
            tracking_url=self.tracking_url, onplay_callback=self.onplay_callback
        )



        if request.has_key("activate_block_id"):
            course_id = request['activate_block_id']
        else:
            course_id = ''

        # ## test용
        # self.caption_info = [
        #     {"src": "http://mme2.npcomms.kr/caption/2015/12/07/7fca2eb8-d1ea-530f-b244-3756b62715db.vtt",
        #      "kind": "captions", "label": "한글자", "srclang": "ko"},
        #     {"src": "http://mme2.npcomms.kr/caption/2015/12/07/7fca2eb8-d1ea-530f-b244-3756b62715db.vtt",
        #      "kind": "captions", "label": "한글자막", "srclang": "ko"}
        # ]
        # self.allow_caption_download = True

        # use_caption_list = ''
        # for caption_list in self.caption_info:
        #     use_caption_list += caption_list['srclang'] + ','




        context = {
            'display_name': self.display_name,
            'allow_download': self.allow_download,
            'allow_caption_download': self.allow_caption_download,
            'video_poster': self.video_poster,
            'source_list': source_list,
            'caption_info': self.caption_info,
            'video_id': self.video_id,
            'video_lang': self.video_lang,
            'preload': self.preload,
            'video_width': self.video_width,
            'video_height': self.video_height,
            'studio_modify': self.studio_modify,
            'course_id': course_id,
            'org_id': self.org_id,

            # 'user_id': self.user_id,
        }



        html = self.render_template('static/html/zplayer_view.html', context)

        frag = Fragment(html)
        frag.add_css(self.load_resource("static/css/zplayer.css"))
        frag.add_javascript(self.load_resource("static/js/zplayer.js"))
        frag.add_javascript(self.load_resource("static/js/lang/ko.js"))
        frag.add_javascript(self.load_resource("static/js/zplayer_view.js"))


        #test용
        # frag.initialize_js('tracking_info')

        #실제용
        # frag.initialize_js('tracking_info')


        frag.initialize_js('zplayerXBlockInitView', {'id_name': self.video_id, 'player_info': player_info,
                                           'source_info': source_list,
                                           'video_poster': self.video_poster, 'tracks': self.caption_info,
                                                     'studio_modify': self.studio_modify})




        # print ";;;;;;;;"
        # print {'id_name': self.video_id, 'player_info': player_info,
        #                                    'source_info': source_list,
        #                                    'video_poster': self.video_poster, 'caption_info': caption_list,
        #        'studio_modify': self.studio_modify}

        return frag

    # @scenario('studio_view')
    def studio_view(self, context=None):
        """
        The secondary view of the XBlock, shown to teachers
        when editing the XBlock.
        """

        source_list = params.get_video_info(self.source_url)

        # player_info = params.get_player_info(lang=self.video_lang, preload=self.preload, width=self.video_width, height=self.video_height)

        use_caption_list = ''
        for caption_list in self.caption_info:
            use_caption_list += caption_list['srclang'] + ','

        context = {
            'display_name': self.display_name,
            'caption_url': 'http://mme.kmooc.kr/caption_convert',
            'delete_url': 'http://mme.kmooc.kr/catpion_delete',
            'allow_download': self.allow_download,
            'allow_caption_download': self.allow_caption_download,
            'video_poster': self.video_poster,
            'source_list': source_list,
            'source_url': self.source_url,
            'caption_info': self.caption_info,
            'video_id': self.video_id,
            'video_lang': self.video_lang,
            'preload': self.preload,
            'video_width': self.video_width,
            'video_height': self.video_height,
            'studio_modify': self.studio_modify,
            'use_caption_list': use_caption_list[:-1],
        }



        html = self.render_template('static/html/zplayer_edit.html', context)

        frag = Fragment(html)

        frag.add_css(self.load_resource('static/css/zplayer_edit.css'))

        frag.add_javascript(self.load_resource('static/js/caption.js')) ### 경로 수정 해야 함

        frag.add_javascript(self.load_resource("static/js/zplayer_edit.js"))
        frag.initialize_js('zplayerXBlockInitStudio')



        return frag

    @XBlock.json_handler
    def save_data(self, data, suffix=''):
        """
        The saving handler.
        """
        try:

            self.display_name = data['display_name']
            self.source_url = data['source_url']
            self.allow_download = True if data['allow_download'] == "True" else False # Str to Bool translation
            self.allow_caption_download = True if data['allow_caption_download'] == "True" else False # Str to Bool translation
            self.video_poster = data['video_poster']
            self.caption_info = data['caption_info']

            self.video_id = data['video_id']
            self.video_lang = data['video_lang']
            self.preload = data['preload']
            self.video_width = data['video_width']
            self.video_height = data['video_height']

            self.studio_modify = True

        except Exception, e:
            pass

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
                    <zplayer />
                    <html_demo><div>Rate the video:</div></html_demo>
                </vertical_demo>
             """),
        ]