// if cookies are disabled remove class 'd-none' from flash message box to display message

if (!navigator.cookieEnabled) {
  document.getElementById( "flash-message-box" ).classList.remove('d-none');
}
