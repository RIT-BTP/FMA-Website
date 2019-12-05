$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/stock-api');
    var numbers_received = [];

    //receive details from server
    socket.on('newprice', function(msg) {
        console.log("Reveiced Payload" + msg);
        $('#dow-chng').html(msg.DOW)
        if (msg.DOW.substring(0,1) == "-"){
            $('#dow-chng').css({'color':'red'});
        } else {
            $('#dow-chng').css({'color':'green'});
        }

        $('#nas-chng').html(msg.NASDAQ)
        if (msg.NASDAQ.substring(0,1) == "-"){
            $('#nas-chng').css({'color':'red'});
        } else {
            $('#nas-chng').css({'color':'green'});
        }

        $('#sp-chng').html(msg.SP500)
        if (msg.SP500.substring(0,1) == "-"){
            $('#sp-chng').css({'color':'red'});
        } else {
            $('#sp-chng').css({'color':'green'});
        }
    });

});
$(function() {
    $('a#refresh').bind('click', function() {
      $.getJSON('/background_refresh',
          function(data) {
        //do nothing
      });
      return false;
    });
  });
