/**
 * Created by muti on 15. 11. 30..
 */
var caption_info_list = [];

$(function(){
	$("#zplayer_caption_submit").click(function(){
        //자막 업로드 모달창 이벤트

		if($("#zplayer_edit_caption_lang").val()){

			overlay();
		}else{
			alert('자막 언어셋을 선택해 주세요.');
			$("#zplayer_edit_caption_lang").focus();
            return false;
		}

	});

	$(".zplayer_edit_caption_lang").change(function(){
        // 자막언어 선택

		$("#caption_lang").val($(".zplayer_edit_caption_lang option:selected").val());
		$("#caption_label").val($(".zplayer_edit_caption_lang option:selected").text());
	})

	$("#caption_upload").click(function(){
        // 자막변환 이벤트 액션

		captionAdd($("#caption_upload_url").val());
	});

	$("#caption_cancel").click(function(){
        // 자박등록 취소

		$("#caption_modal_file").val('');
		set_default();
        overlay();
	});

        //todo 클릭시에도 이벤트가 안걸린다 확인 할것
        // devstack, fullstack에 설치하여 해당 디자인 등을 수정해야 한다.
        // 그후 코스 저장 크래킹로그 연동 부분을 처리하면 끝이다 ㅠㅠ
        // 체크사항: 저장이 끝난 경우.. 코스에 연동을 어떨게 하지???? videojs, 기본 코스 등록과 비교해야 한다.
});



var captionAdd = function (caption_url) {
    var caption_form = new FormData();

	$.each($("#caption_modal_file")[0].files, function(i, file){
        caption_form.append('uploadFile', file);


    });

    caption_form.append('clang', $("#caption_lang").val());
    caption_form.append('clabel', $("#caption_label").val());

    console.log(caption_form);

    //caption_form.append("caption_modal_file", file);

    var caption_name = $("#caption_modal_file").val();

    $.ajax({
        url: caption_url,
        type: "post",
        dataType: "text",
        data: caption_form,
        processData: false,
        contentType: false,
        success: function(data, textStatus, jqXHR){

            try{
                var jdata = JSON.parse(data);
            }catch(e){
                var jdata = data;
            }

            jdata = jdata.data;

            if(jdata.caption_result == true){
            	var caption_data = {
            		kind: 'captions', src: jdata.caption_url, srclang: jdata.clang, label: jdata.clabel
            	};
            	caption_data = JSON.stringify(caption_data);
            }else{
            	var caption_data = "";
            }



            $("#caption_modal_file").val('');

            var caption_info = "<input type='hidden' name='caption_info[]' value='" + caption_data +"'>";

            if(caption_data){
            	$("#caption_list").append(
                    "<li>" + jdata.clabel + '(' + jdata.clang + ') : ' + jdata.caption_url +
                    caption_info +
                        "<button class='input setting-input caption-del' data-lang='"+jdata.clang+"' data-path='"+
                    jdata.caption_path +"' onclick='remote_caption_delete($(this))'>자막삭제</button>" +
                    '</li>'
                );
            }

            $("#zplayer_edit_caption_lang :selected").prop('disabled', true);

            set_default();
            overlay();


        }, error: function(jqXHR, textStatus, errorThrown){
        	alert('변환을 실패하였습니다.');
            alert(errorThrown.message);

        },
        complete: function(){

        }
    });
};

var set_default = function(){
    /**
     * 초기화 처리
     */
	$("#caption_modal_file").val('');
    $("#caption_lang").val('');
    $("#caption_label").val('');
    $("#zplayer_edit_caption_lang").val('').attr("selected", "selected");
}


var overlay = function() {
    /**
     * 모달 toggle function
     * @type {Element}
     */
	//el = document.getElementById("caption_modal");
	//el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}

var remote_caption_delete = function(del_obj){

    if(confirm('해당 자막을 삭제하시겠습니까?\n영구적으로 삭제됩니다.')){
        var delete_url = $("#delete_url").val();
        var caption_path = del_obj.data("path");
        $.ajax({
            url: delete_url,
            type: "post",
            data: "caption_path=" + caption_path,
            dataType: "text",
            success: function(data, textStatus, jqXHR){
                try{
                    var jdata = JSON.parse(data);
                }catch(e){
                    var jdata = data;
                }

                if(jdata.message == 'OK'){
                    alert('삭제되었습니다.');
                    $("#zplayer_edit_caption_lang option[value='"+del_obj.data("lang")+"']").prop('disabled', false);
                    del_obj.parent().remove();



                }else{
                    alert('해당 자막을 삭제하지 못하였습니다.');
                }
            },error: function(jqXHR, textStatus, errorThrown){
                alert('삭제처리가 진행되지 않았습니다.\n재시도해주세요.');
            }

        });
    }

}
