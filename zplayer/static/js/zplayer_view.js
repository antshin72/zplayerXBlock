/**
 * Created by muti on 15. 11. 27..
 */

/**
 * zplayer Content load
 * @param id_name string node name
 * @param player_info json player property
 * @param source_info json array movie streaming url
 * @param video_title course string title
 * @param video_poster string video thumbnail url
 * @param caption_info json array capiton property
 */
var initContent = function(id_name, player_info, source_info, video_title, video_poster, caption_info){
    var zp = zplayer(id_name, player_info).clip({
        source: source_info,
        title: video_title,
        poster: video_poster,
        tracks: caption_info
    });
}


var zplayerXBlockInitView = function(runtime, element, params) {
    /* Weird behaviour :
     * In the LMS, element is the DOM container.
     * In the CMS, element is the jQuery object associated*
     * So here I make sure element is the jQuery object */
    if(element.innerHTML) element = $(element);

    initContent(params.id_name, params.player_info, params.source_info, params.video_title, params.video_poster, params.caption_info);

}
