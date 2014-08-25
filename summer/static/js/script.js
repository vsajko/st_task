
// helper for url making
function EncodeQueryData(data){
    var ret = [];
    for (var d in data)
        ret.push(encodeURIComponent(d) + "=" + encodeURIComponent(data[d]));
    return ret.join("&");
}

$(document).ready(function() {
    myurlobj = window.getQueryParameters();

    // toplist select by channel
    $("#selectfeed").change(function() {
        var newfeedlink = $(this).val();
        console.log(newfeedlink);
        if( newfeedlink != ''){
            myurlobj.feedlink = newfeedlink
        }else if(newfeedlink === ''){
            delete myurlobj.feedlink
        }
        console.log(myurlobj);
        var newsearch = EncodeQueryData(myurlobj);
        console.log(newsearch)
            window.location.search = newsearch;

    });


    // change channel status active/inactive
    $('.change-feed-status').click(function(){
        var catid;
        feedid = $(this).attr("feedid");
        btn = $('button.change-feed-status[feedid|="' + feedid + '"]')
            $.get('/summer/change_feed_status/', {'feedid': feedid}, function(data){
                if(data == 'True'){
                    btn.addClass('btn-success').removeClass('btn-default');
                }else{
                    btn.addClass('btn-default').removeClass('btn-success')
                }
                btn.text(data);
            });
    });

    // mark active page in nav
    var url = window.location;
    $('ul.nav a[href="'+ url +'"]').parent().addClass('active');
    $('ul.nav a').filter(function() {
        return this.href == url;
    }).parent().addClass('active');


});
