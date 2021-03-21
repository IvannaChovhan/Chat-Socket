$(function() {
    $('#sendBtn').bind('click', function() {
        var msg = document.getElementById("msg")
        var value = msg.value
        msg.value = ""
        $.getJSON('/send_message',
            {val:value},
            function(data) {
                
            });
        });
});

window.onload = function(){
    var update_loop = this.setInterval(update_message, 1000);
    update_message()
}



function update_message(){
    fetch('/get_messages')
        .then(function(response){
            return response.json();
        }).then(function(text){
            var messages = "";
            for (value of text['messages']){
                messages = messages + value
            }
            document.getElementById("test").innerHTML = messages;
        });
};