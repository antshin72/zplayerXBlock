function zplayerXBlockInitStudio(runtime, element) {

    $(element).find('.action-cancel').bind('click', function() {
        runtime.notify('cancel', {});
    });

    $(element).find('.action-save').bind('click', function() {
        var data = {
            'display_name': $("#zplayer_edit_display_name").val(),
            'source_url': $("#zplayer_edit_url").val(),
            'allow_download': $("#zplayer_edit_allow_download").val(),
            'allow_caption_download': $("#zplayer_edit_allow_caption_download").val(),
            'video_poster': $("#zplayer_edit_poster").val(),
            'studio_modify': "True",
            'caption_info': [],

            'video_id': $("#video_id").val(),
            'video_width': $("#video_width").val(),
            'video_height': $("#video_height").val(),
            'video_lang': $("#video_lang").val(),
            'preload': "auto",
        };


        var caption_info = [];
        $.each($("input[name='caption_info[]']"), function(i, data){
            caption_info[i] = JSON.parse($(data).val());

        });

        data['caption_info'] = caption_info;


        runtime.notify('save', {state: 'start'});

        var handlerUrl = runtime.handlerUrl(element, 'save_data');
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.result === 'success') {
                runtime.notify('save', {state: 'start'});
                // Reload the whole page :
                // window.location.reload(false);
                $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
                  runtime.notify('save', {state: 'end'});
                });
                window.location.reload(false);
            } else {
                runtime.notify('error', {msg: response.message});
            }
        });
    });
}
