$.ajax({
  type: "GET",
  dataType: "json",
  url: "http://localhost:5000/random_color",

  success: function(data) {
    console.log(data);
  }
})
