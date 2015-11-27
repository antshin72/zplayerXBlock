# XBlock Zplayer 구성 작업
## 항목
- Student Viewer	프론트 뷰잉 플레이어
- Studio Viewer		자막파일 등록

## xblock-sdk에 zplayer 설정하기
- requirements.txt 파일 구성함 : 해당 파일(또는 별도파일)에 아래와 같은 코드를 입력하고 실행
    requirements.txt 내용
    
    ```
    requests
    -e .

    ```
- xblock-sdk에 적용
    
    cd ../xblock-sdk
    workon xblock-sdk
    pip install -r requirements.txt
    
    
    
    - 설치결과
            
        (xblock-sdk)sinyeong-gyuui-MacBook-Pro-2:zplayer muti$ pip install -r             requirements.txt 
Obtaining file:///Users/muti/PycharmProjects/zplayer (from -r requirements.txt (line 2))
Requirement already satisfied (use --upgrade to upgrade): requests in /Users/muti/.virtualenvs/xblock-sdk/lib/python2.7/site-packages (from -r requirements.txt (line 1)) .... 중략 .....

**Successfully installed xblock-zplayervideo**


## xblock 실행하기
    workon xblock-sdk
    cd xblock-sdk
    python manage.py runserver
    
localhost:8000 으로 접속

## xblock 제작하기
### xblock subclass 구성
zplayer xblock의 구성을 위해서는 우선적으로 아래와 같은 구조의 파일을 구성해야 한다.
<zplayervideo> 태그를 사용하여 등록함.
위의 태그에 대한 subclass로 ZplayerVideoBlock 를 선언하고, 프로젝트 최상단에 zplayer.py 파일을 구성함

파일 내용

```
from xblock.core import XBlock
from xblock.fields import Scope, Integer, String

class ZplayerVideoBlock(XBlock):
    """
    An XBlock providing oEmbed capabilities for video
    """

    href = String(help="URL of the video page at the provider", default=None, scope=Scope.content)
    maxwidth = Integer(help="Maximum width of the video", default=800, scope=Scope.content)
    maxheight = Integer(help="Maximum height of the video", default=450, scope=Scope.content)
```

파라미터의 정의는 위와 같이 정의한다. (String / Integer emd)

### View 구성 (HTML, templates, fragments)
코스에 비디오 플레이어를 embed하기 위해서는 XBlock은 HTML코드를 가져와야 한다.
심플예제에서는 vimeo의 oEmbed를 사용함.(참고용으로만)

#### ZplayerVideoBlock을 선언
zplayer.py 에 선언함.
확장 플레이어에서는 url등의 소스 등에 대한 값만을 정의하여 내부 연동을 처리한다.
XBlocks에서 사용해야 할 View의 정의는 ZplayerVideoBlock.student_view() 메소드이다.

#### Static 파일 구성함.
XBlock에서는 템플릿/HTML/CSS/Javascript등을 파이썬의 pkg_resources_module를 사용한다.
**기본구성**

static 디렉토리 하위에 js, css, html 폴더를 구성한다. (반드시 구성되어야 하는 구성요소는 아니나 관습적으로 pkg_resources에서 사용하는 형식으로 XBlock을 구성하는 것을 가이드 한다.)

zplayer.html

    <video id="zplayer" class="zplayer"></video>

- zid : video tag ID값 선언

- play_params : zplayer 속성에 대한 json

- video_info : 동영상 정보, 이미지, 자막 정보 등에 대한 json

#### workbench(scenarios) 로딩 처리
위에 정의된 xblock 구성이 로딩이 되기 위해서는 워크벤치 시나리오가 구성되어야 하며 해당 구성은 xml구성 방식으로 <zplayervideo> 태그로 구성이 되도록 한다.

	<vertical_demo>
		<zplayervideo />
	<vertical_demo>
	
	위의 선언은 zplayer.py에 staticmethod로 구성되어야 한다.
	
#### XBlock (entry point) 등록
workbench까지 적용된 Xblock을 적용하기 위해




##XBlock에 zplayerXBlock 적용하는 방법
현재, xblock을 적용 하는 방법은 devstack/fullstack에 적용 하는 방법과 xblock-sdk에 적용 하는 방법이 있다.
simplevideo 튜토리얼에서는 pip install -r requirement.txt 명령으로 xblock-sdk에 인식을 시켜 작업을 한다.
해당 구성과 마찬가리고 해도 되나 현재 패키지 방식으로 해놓은 관계로
pip install zplayerXBlock/ 처럼 처리하도록 해놨다.. (setup.py 가 있으므로)

