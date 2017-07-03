/**
 * Created by jesse on 6/11/2017.
 */

// start function needs to initialize the gapi.auth2 object.
// this will then check with google that the client id is valid for the javascript origin.
function start() {
  gapi.load('auth2', function() {
    console.log("auth2 loading")
    auth2 = gapi.auth2.init({
        client_id: '301799514828-1k6adibgcnh87aimo194mvfbkk4p0t13.apps.googleusercontent.com',
      // Scopes to request in addition to 'profile' and 'email'
      //scope: 'additional_scope'
    });
  });
}

// sign in callback as needed for the Google Sign in
// forwards the one time use code back to the server
// we should receive a response from the server with 200 ok
function signInCallback(authResult) {
    if (authResult["code"]){
        // $("#signInButton").attr('style', "display: none");
        //
        $.ajax({
            type: "POST",
            url: "/google_login?state=" + state,
            //headers: {"X-Requested-With": "XMLHttpRequest"},
            contentType: "application/octet-stream; charset=utf-8",
            processData: false,
            data: authResult["code"],
            success: function (result) {
                console.log("Success response from server")
                window.location = result;
            }
        })
    }
    else{
        console.log("There was an error")
    }
}


$(document).ready(function () {
    console.log("Document Ready")
    start()
   $('#signInButton').click(function() {
    // signInCallback defined in step 6.
    auth2.grantOfflineAccess().then(signInCallback);


  });


})









