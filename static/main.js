
function check(){
    $.get("/getStatus").done(function( data ){
        $('.servers.online ul').html('')
        $('.servers.offline ul').html('')
        data['data'].forEach(function(server) {
            if (server['durum'] == "Online"){
                el = "<li><span class=\"name\">"+server['name']+"</span><span class=\"online\">"+server['players']+"/"+server['maxplayers']+"</span></li>"
                $('.servers.online ul').append(el)
            } else{
                el = "<li><span class=\"name\">"+server['name']+"</span></li>"
                $('.servers.offline ul').append(el)
            }
        }, this);
    });
}

$(function(){
    check();
    setInterval(function(){
        check();
    }, 5000);
});