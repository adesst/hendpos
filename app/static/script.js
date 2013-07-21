var wsUri = "ws://localhost:5000/websocket";
var output = {'log' : false, 'status' : false,};

function init()
{
  output.log = document.getElementById("log");
  output.status = document.getElementById("status");
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
  writeToScreen("CONNECTED", output.status);
  doSend("{'mode' : 'init'}");
}

function onClose(evt)
{
  writeToScreen("DISCONNECTED", output.status);
}

function onMessage(evt)
{
  writeToScreen('<span style="color: blue;">RESPONSE: ' + evt.data+'</span>', output.log);
  //websocket.close();
}

function onError(evt)
{
  writeToScreen('<span style="color: red;">ERROR:</span> ' + evt.data, output.status);
}

function doSend(message)
{
  writeToScreen("SENT: " + message, output.log); 
  websocket.send(message);
}

function writeToScreen(message, screen)
{
  var pre = document.createElement("p");
  pre.style.wordWrap = "break-word";
  pre.innerHTML = message;
  screen.appendChild(pre);
}

$("#new").click(function(){
  window.location = "{{ url_for('user_new') }}"
});
