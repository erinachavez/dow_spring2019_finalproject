
window.onload = function () {
  var lines = document.querySelectorAll('#poem p');

  if (lines.length != 0) {
    var i=0, c = setInterval(function() {
      lines[i].style.opacity = 1;
      i++;

      if (i >= lines.length){
        document.getElementById("fade_in").style.opacity = 1;
        clearInterval(c);
      };
    }, 1000);
  }
}
