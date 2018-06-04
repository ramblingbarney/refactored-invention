//set cookie expiry vars for session user login logout
var today = new Date();
var expiry = new Date(today.getTime() + 30 * 24 * 3600 * 1000); // plus 30 days
var expired = new Date(today.getTime()); // plus 30 days

// When the page is refreshed the currently logged in user details are reloaded from the cookie

window.onload = function() {

  if (getCookie('user_name')) {

    document.getElementById( "player-name" ).innerText = getCookie('user_name');
    document.getElementById( "total-points" ).innerText = getCookie('total_score');

  }

}

// set cookie value
function setCookie(name, value) {
  document.cookie=name + "=" + escape(value) + "; path=/; expires=" + expiry.toGMTString();
}

// delete cookie value
function deleteCookie(name) {
  document.cookie=name + "=null; path=/; expires=" + expired.toGMTString();
}

//get cookie value
function getCookie(name) {
    var re = new RegExp(name + "=([^;]+)");
    var value = re.exec(document.cookie);
    return (value != null) ? unescape(value[1]) : null;
}

// login request to the login app route

function login(url,inputName) {

  // The data we are going to send in our request

  let data = {
    userName: inputName
  }

  // The parameters we are gonna pass to the fetch function

  let fetchData = {
      method: 'POST',
      body: JSON.stringify(data),
      headers: new Headers()
  }

  fetch(url,fetchData)
    .then(
      function(response) {
        if (response.status !== 200) {
          console.log('Looks like there was a problem. Status Code: ' +
            response.status);
          return;
        }

        // Examine the text in the response
        response.json().then(function(data) {

          if (data){

            // store the response data values in the cookie
            setCookie('user_name', data.user_name);
            setCookie('total_score', data.total_score);

            // Update the UI with values stored in the cookie
            logInUpdateUI();

          }



        });
      }
    )
    .catch(function(err) {
      console.log('Fetch Error :-S', err);
    });
}

function logInUpdateUI() {

  // display username in the nav bar
  document.getElementById( "player-name" ).innerText = getCookie('user_name');
  // display user score in the nav bar
  document.getElementById( "total-points" ).innerText = getCookie('total_score');
  // remove username from the login input box
  document.getElementById( "login-name" ).value = "";

}

function logOutUpdateUI(){

  // update the UI to remove users name, total score from the nav bar
  document.getElementById( "player-name" ).innerText = "";
  document.getElementById( "total-points" ).innerText = "";

}

function logOut() {

  // store users total score in file
  writeOutDataToFile('/update_score',[getCookie('user_name'),getCookie('total_score'),0]);
  // delete user's username from the users cookie
  deleteCookie('user_name');
  // delete user's total score from the users cookie
  deleteCookie('total_score');
  // update the UI
  logOutUpdateUI();

}

function writeOutDataToFile(url,writeData) {

  // The data we are going to send in our request

  let data = {
    writeData: writeData
  }

  // The parameters we are gonna pass to the fetch function

  let fetchData = {
      method: 'POST',
      body: JSON.stringify(data),
      headers: new Headers()
  }

  fetch(url,fetchData)
    .then(
      function(response) {
        if (response.status !== 200) {
          console.log('Looks like there was a problem. Status Code: ' +
            response.status);
          return;
        }

      }
    )
    .catch(function(err) {
      console.log('Fetch Error :-S', err);
    });
}
