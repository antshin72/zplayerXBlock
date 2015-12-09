/**
 * Created by muti on 15. 11. 27..
 */


var zp;

var zplayerXBlockInitView = function(runtime, element, params) {
    /* Weird behaviour :
     * In the LMS, element is the DOM container.
     * In the CMS, element is the jQuery object associated*
     * So here I make sure element is the jQuery object */
    if(element.innerHTML) element = $(element);



    try{
        zplayer(params.id_name, params.player_info).clip({
            source: params.source_info,
            title: params.video_title,
            poster: params.video_poster,
            tracks: params.tracks,
        });
    }catch(e){
        console.log('Player Initialize Exception: ', e.message);

        zplayer(params.id_name, params.player_info).clip({
            source: params.source_info,
            title: params.video_title,
            poster: params.video_poster,
            //tracks: params.tracks
        });
    }

    var edxloggedin = getCookie('edxloggedin');


    var sessionid = getCookie('sessionid');
    $("#sessionid").val(sessionid);


    $("#edxloggin").val(edxloggedin);



    //var user_info = JSON.parse(getCookie('edx-user-info').stripComma().stripSlashes());
    var user_info = getCookie('edx-user-info').stripComma().stripSlashes();
    //var user_info = getCookie('edx-user-info').stripSlashes();
    //var user_info = getCookie('edx-user-info');
    $("#username").val(user_info);



    var lms_path = location.pathname;
    $("#path").val(lms_path);

}


var tracking_info = function(runtime, element){
    alert('aaaa');
    var edxloggedin = getCookie('edxloggedin');


    var sessionid = getCookie('sessionid');
    $("#sessionid").val(sessionid);


    $("#edxloggin").val(edxloggedin);



        var user_info = JSON.parse(getCookie('edx-user-info'));
        $("#username").val(user_info.username);



        var lms_path = location.pathname;
        $("#path").val(lms_path);

}


function getCookie( name ){
  	var nameOfCookie = name + '=';
  	var x = 0;
    while ( x <= document.cookie.length ) {
        var y = (x+nameOfCookie.length);
            if ( document.cookie.substring( x, y ) == nameOfCookie ) {
                if ( (endOfCookie=document.cookie.indexOf( ';', y )) == -1 )
                    endOfCookie = document.cookie.length;
                    return unescape( document.cookie.substring( y, endOfCookie ) );
                }
                x = document.cookie.indexOf( ' ', x ) + 1;
                if ( x == 0 )
                    break;
        }
    return '';
}

String.prototype.stripSlashes = function(){
    return this.replace(/\\(.)/mg, "$1");
}

String.prototype.stripComma = function(){
    return this.replace(/\\054/g, ',');
}