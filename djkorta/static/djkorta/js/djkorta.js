function CCNumKeyUp() {
    var n = $(this).val();
    $.each($('.card').addClass('disabled'), function(i){
        if(n.match($(i).attr('data-match'))) {
            $(i).removeClass('disabled');
        }
    });
}
