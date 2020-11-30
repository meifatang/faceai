var current_people;
var current_datetime;

setInterval(function(){ 

  $.post( "/find", function( data ) {
    $( "#username1" ).html( data["data"][data["data"].length-3]["username"] );
    $( "#datetime1" ).html( data["data"][data["data"].length-3]["datetime"] );

    $( "#username2" ).html( data["data"][data["data"].length-2]["username"] );
    $( "#datetime2" ).html( data["data"][data["data"].length-2]["datetime"] );

    $( "#username3" ).html( data["data"][data["data"].length-1]["username"] );
    $( "#datetime3" ).html( data["data"][data["data"].length-1]["datetime"] );

    $( "#avator").attr("src", data["data"][data["data"].length-1]["image_url"] )

    if (current_people != data["data"][data["data"].length-1]["username"] &&
        current_datetime != data["data"][data["data"].length-1]["datetime"]) {
          let utterance = new SpeechSynthesisUtterance(data["data"][data["data"].length-1]["username"]);
          speechSynthesis.speak(utterance);
        }

    current_people = data["data"][data["data"].length-1]["username"];
    current_datetime = data["data"][data["data"].length-1]["datetime"];
  });

}, 1000);