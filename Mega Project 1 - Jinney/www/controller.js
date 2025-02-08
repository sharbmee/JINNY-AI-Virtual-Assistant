$(document).ready(function () {

    // Display Speak message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {

        $(".siri-message li:fi").text(message);
        $('.siri-message').textillate('start');
    }

    //Display Hood
    eel.expose(ShowHood);

    function ShowHood() {
        $("#Oval").attr("hidden", false); // Show Oval
        $("#SiriWave").attr("hidden", true); // Hide SiriWave
    }

    // // Test Button
    // $("#TestButton").click(function () {
    //     eel.call_showhood();
    // });

});