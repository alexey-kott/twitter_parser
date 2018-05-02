function form_tweet(tweet) {
    var is_retweet = '';
    if (tweet.is_retweet) {
        is_retweet = "ReTweet: "
    }
    var elem = '';
    return elem;
}

var web_socket = new WebSocket('ws://' + window.location.host + '/');

web_socket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    if (data.action === 'complete') {
        $(".tweet-loading").fadeOut(100);
        return false;
    }

    if (data.action === 'user_not_exist') {
        $(".tweet-loading").fadeOut(100);
        $("#tweets").append('<span class="error">USER DOES NOT EXIST</span>')
        return false;
    }

    // ДАННЫЕ ЗАБИРАТЬ ЗДЕСЬ
    console.log(data);

    data.forEach(function (tweet, i, data) {
        $("#tweets").append(form_tweet(tweet))


    })
};

web_socket.onclose = function (e) {
    web_socket = new WebSocket('ws://' + window.location.host + '/');

};

$('#username-input').focus();
$('#username-input').on("keyup", function (e) {
    if (e.keyCode === 13) { // enter, return
        $('#username-submit').click();
    }
})

$('#username-submit').on("click", function (e) {
    var username = $('#username-input').val()
    if (username === '') return 0;

    if (web_socket.readyState === 3) {
        web_socket = new WebSocket('ws://' + window.location.host + '/');
    } else {
        web_socket.send(JSON.stringify({
            'username': username
        }))
    }

    $(".tweet-loading").fadeIn(100);
    $("#tweets").empty()


})