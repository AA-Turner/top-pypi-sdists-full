bodyHtml = "<div id='status'></div><br>" +
           "<a href='javascript:pyloco.disconnect()'>" +
           "    Disconnect</a>";

document.body.innerHTML = bodyHtml;

pyloco.onOpen(function openHandler (evt) {
    var status = document.getElementById("status")
    status.innerHTML = "Pyloco connection open";
});

pyloco.onClose(function closeHandler (evt) {
    var status = document.getElementById("status")
    status.innerHTML = "Pyloco connection closed";
});

pyloco.onMessage("pyloco", "task", function messageHandler (msgId, ts, msg) {
    var status = document.getElementById("status")
    status.innerHTML = "Pyloco message: " + JSON.stringify(msg);
});

pyloco.onError(function errorHandler (evt) {
    var status = document.getElementById("status")
    status.innerHTML = "Pyloco error happend";
});
