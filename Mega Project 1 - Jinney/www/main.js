$(document).ready(function () {

    $('.text').textillate({
        loop: true, // Repeat the animation
        sync: true,
        in: {
          effect: 'fadeInDown', // Entrance animation
          delay: 20,           // Delay between characters
        },
        out: {
          effect: 'fadeOutUp',  // Exit animation
          delay: 20,            // Delay between characters
        },
      });

    //Siri configuration
    // Ensure the script runs only once
    if (!window.siriWaveInstance) {
        const siriWave = new SiriWave({
        container: document.getElementById("siri-container"), // Target container
        width: 800, // Explicit dimensions
        height: 200,
        style: "ios9", // Style of the wave
        amplitude: 1, // Numeric value for amplitude
        speed: 0.3, // Numeric value for speed
        autostart: true, // Automatically start the wave
        });
        // Save instance globally to prevent duplication
        window.siriWaveInstance = siriWave;
    }

  //siri message animation
  $('.Siri-message').textillate({
    loop: true, // Repeat the animation
    sync: true,
    in: {
      effect: 'fadeInUp', // Entrance animation
      sync: true,
    },
    out: {
      effect: 'fadeOutUp',  // Exit animation
      sync: true,
    },
  });

  // Expose DisplayMessage to Python
  eel.expose(DisplayMessage);

  // Function to display messages from Python
  function DisplayMessage(message) {
      console.log("Message received:", message); // Debug log
      $(".siri-message").text(message); // Updates the Siri message text
      $('.siri-message').textillate('start'); // Start text animation (if textillate is loaded)
  }

  //mic button click animation
  $("#MicBtn").click(function () {
    console.log("Mic button clicked");
    eel.playAssistantSound();
    $("#Oval").attr("hidden", true);  // Hides Oval
    $("#SiriWave").attr("hidden", false); // Shows SiriWave
    eel.allCommand()(); // This triggers the command function only once
    });

    function doc_keyUp(e) {
      // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

      if (e.key === 'j' && e.metaKey) {
          eel.playAssistantSound()
          $("#Oval").attr("hidden", true);
          $("#SiriWave").attr("hidden", false);
          eel.allCommand()();
      }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // to play assisatnt 
    function PlayAssistant(message) {
      if (message.trim() !== "") {
  
          $("#Oval").hide();
          $("#SiriWave").show();
  
          // Send message to Python and wait for a response
          eel.allCommand(message)(function(response) {
              console.log("Assistant Response:", response);
  
              $("#ChatBox").val("");  // Clear ChatBox
              $("#MicBtn").show();
              $("#SendBtn").hide();   // Ensure SendBtn is hidden after sending
          });
      }
    }
  

    // toogle fucntion to hide and display mic and send button 
    function ShowHideButton(message) {
      if (message.trim().length === 0) {
          $("#MicBtn").show();   // Show Mic button when no text is entered
          $("#SendBtn").hide();  // Hide Send button when input is empty
      } else {
          $("#MicBtn").hide();   // Hide Mic button when text is entered
          $("#SendBtn").show();  // Show Send button when input is filled
      }
    }


    // key up event handler on text box
    $("#ChatBox").keyup(function () {

      let message = $("#ChatBox").val();
      ShowHideButton(message)
  
    });
  
    // send button event handler
    $("#SendBtn").click(function () {
    
      let message = $("#ChatBox").val()
      PlayAssistant(message)
  
    });

    // enter press event handler on chat box
    $("#ChatBox").keypress(function (e) {
      key = e.which;
      if (key == 13) {
          let message = $("#ChatBox").val()
          PlayAssistant(message)
      }
    });



});