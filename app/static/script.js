var wsUri = "ws://localhost:5000/websocket";
var output = '';

var Keys = {
    _F1 : 112,                  
    _F2 : 113,
    _F3 : 114,
    _F4 : 115,
    _F5 : 116,
    _F6 : 117,
    _F7 : 118,
    _F8 : 119,
    _F9 : 120,
    _F10 : 121,
    _F11 : 122,
    _F12 : 123,
    _ENTER : 13,
    _SPACE : 32,
    _ESC_KEY : 27,
};

function init()
{
    output = document.getElementById("log");
    jQuery("button#check_uid").click(function(){ doSend("{'mode': 'check_uid'}"); });
    jQuery("button#sell").click(function(){ doSend("{'mode': 'sell'}"); });
    jQuery("button#top_up").click(function(){ doSend("{'mode': 'top_up'}"); });
    //jQuery("button#new").click(function(){ doSend("{'mode': 'new'}"); });
    jQuery("button#renew").click(function(){ doSend("{'mode': 'renew'}"); });
    jQuery("button#close").click(function(){ websocket.close(); });
    jQuery("button#reconnect").click(function(){ testWebSocket(); });
    testWebSocket();
}

function testWebSocket()
{
    websocket = new WebSocket(wsUri);
    websocket.onopen = function(evt) { onOpen(evt) };
    websocket.onclose = function(evt) { onClose(evt) };
    websocket.onmessage = function(evt) { onMessage(evt) };
    websocket.onerror = function(evt) { onError(evt) };
}

function onOpen(evt)
{
    writeToScreen("CONNECTED");
    doSend("{'mode' : 'init'}");
}

function onClose(evt)
{
    writeToScreen("DISCONNECTED");
}

function onMessage(evt)
{
    writeToScreen('<span style="color: blue;">RESPONSE: ' + evt.data+'</span>');
    //websocket.close();
}

function onError(evt)
{
    writeToScreen('<span style="color: red;">ERROR:</span> ' + evt.data);
}

function doSend(message)
{
    writeToScreen("SENT: " + message); 
    websocket.send(message);
}

function writeToScreen(message)
{
    var pre = document.createElement("p");
    pre.style.wordWrap = "break-word";
    pre.innerHTML = message;
    output.appendChild(pre);
}

function hideFlashes()
{
    jQuery("ul.flashes").slideUp(1000);
}

jQuery(document).ready(function(){
    if ( jQuery("ul.flashes").length > 0 )
    {
        setTimeout(hideFlashes,3000); 
    }
});
