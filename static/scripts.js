$(document).ready(function(){
    var x = 0;
    var y = 0;
    var z = 0;

    $("#plus_x_100").on("click",add_x_100);
    $("#min_x_100").on("click",sub_x_100);

    function add_x_100(){
      if (x<900){x += 100;}
      output = Math.abs(parseInt(x/100));
      $("#x_100").html(output);
      if(x>=0){$("#x_pm").text("+")}
    }

    function sub_x_100(){
      if (x>-900){x -= 100;}
      output = Math.abs(parseInt(x/100));
      $("#x_100").html(output);
      if(x<0){$("#x_pm").text("-")}
    }


  });