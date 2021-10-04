$(document).ready(function(){
    var x = 0;
    var y = 0;
    var z = 0;

    var sign_x = 1;
    var sign_y = 1;
    var sign_z = 1;

    $("#plus_x_100").on("click",add_x_100);
    $("#min_x_100").on("click",sub_x_100);
    $("#plus_x_10").on("click",add_x_10);
    $("#min_x_10").on("click",sub_x_10);
    $("#plus_x_1").on("click",add_x_1);
    $("#min_x_1").on("click",sub_x_1);

    $("#plus_y_100").on("click",add_y_100);
    $("#min_y_100").on("click",sub_y_100);
    $("#plus_y_10").on("click",add_y_10);
    $("#min_y_10").on("click",sub_y_10);
    $("#plus_y_1").on("click",add_y_1);
    $("#min_y_1").on("click",sub_y_1);

    $("#plus_z_100").on("click",add_z_100);
    $("#min_z_100").on("click",sub_z_100);
    $("#plus_z_10").on("click",add_z_10);
    $("#min_z_10").on("click",sub_z_10);
    $("#plus_z_1").on("click",add_z_1);
    $("#min_z_1").on("click",sub_z_1);

    $("#x_pm").on("click", reverseX);
    $("#y_pm").on("click", reverseY);
    $("#z_pm").on("click", reverseZ);
    
    $("#launch-btn").on("click", launchProbe);
    

    /* ----------- X ------------- */

    function add_x_100(){
      if (x<900){
        x += 100;
      } else {
        x -= 900;
      }

      const output = Math.abs(parseInt(x/100));
      $("#x_100").html(output);
      if(x>=0){$("#x_pm").text("+")}
    }

    function sub_x_100(){
      if (x>=100){x -= 100;}
      const output = Math.abs(parseInt(x/100));
      $("#x_100").html(output);
    }

    function add_x_10(){
      var mid = grabMid(x);
      if (mid<9){x += 10;}
      const output = grabMid(x);
      $("#x_10").html(output);
    }

    function sub_x_10(){
      var mid = grabMid(x);
      if (mid>0){x -= 10;}
      const output = grabMid(x);
      $("#x_10").html(output);
    }

    function add_x_1(){
      var low = grabLow(x);
      if (low<9){x += 1;}
      const output = grabLow(x);
      $("#x_1").html(output);
    }

    function sub_x_1(){
      var low = grabLow(x);
      if (low>0){x -= 1;}
      const output = grabLow(x);
      $("#x_1").html(output);
    }


    /* ----------- Y ------------- */

    function add_y_100(){
      if (y<900){
        y += 100;
      } else {
        x -= 900;
      }
      const output = Math.abs(parseInt(y/100));
      $("#y_100").html(output);
      if(y>=0){$("#y_pm").text("+")}
    } 


    function sub_y_100(){
      if (y>=100){y -= 100;}
      const output = Math.abs(parseInt(y/100));
      $("#y_100").html(output);
    }

    function add_y_10(){
      var mid = grabMid(y);
      if (mid<9){
        y += 10;
      } else {
        x -= 90;
      }
      const output = grabMid(y);
      $("#y_10").html(output);
    } 

    function sub_y_10(){
      var mid = grabMid(y);
      if (mid>0){y -= 10;}
      const output = grabMid(y);
      $("#y_10").html(output);
    }

    function add_y_1(){
      var low = grabLow(y);
      if (low<9){
        y += 1;
      } else {
        x -= 9;
      }
      const output = grabLow(y);
      $("#y_1").html(output);
    } 

    function sub_y_1(){
      var low = grabLow(y);
      if (low>0){y -= 1;}
      const output = grabLow(y);
      $("#y_1").html(output);
    }


    /* ----------- Z ------------- */

    function add_z_100(){
      if (z<900){
        z += 100;
      } else{
        x -= 900;
      }
      const output = Math.abs(parseInt(z/100));
      $("#z_100").html(output);
      if(z>=0){$("#z_pm").text("+")}
    }

    function sub_z_100(){
      if (z>=100){z -= 100;}
      const output = Math.abs(parseInt(z/100));
      $("#z_100").html(output);
    }

    function add_z_10(){
      var mid = grabMid(z);
      if (mid<9){
        z += 10;
      } else {
        x -= 90;
      }
      const output = grabMid(z);
      $("#z_10").html(output);
    } 

    function sub_z_10(){
      var mid = grabMid(z);
      if (mid>0){z -= 10;}
      const output = grabMid(z);
      $("#z_10").html(output);
    }

    function add_z_1(){
      var low = grabLow(z);
      if (low<9){
        z += 1;
      } else {
        x -= 9;
      }
      const output = grabLow(z);
      $("#z_1").html(output);
    } 

    function sub_z_1(){
      var low = grabLow(z);
      if (low>0){z -= 1;}
      const output = grabLow(z);
      $("#z_1").html(output);
    }
    


    /* ----------------- */

    function grabMid(input){
      output = parseInt(input/10)%10;
      return output;
    }

    function grabLow(input){
      output = input%10;
      return output;
    }

    function reverseX(){
      if (sign_x==1){ 
        $("#x_pm").attr("src","static/images/minus_btn.png");
        sign_x = -1;
        console.log("sign_x = ",sign_x);
        return
      }
      if (sign_x==-1){ 
        $("#x_pm").attr("src","static/images/plus_btn.png");
        console.log("src = ","{{url_for('static', filename='images/plus_btn.png') }}");
        sign_x = 1;
        console.log("sign_x = ",sign_x);
        return
      }
    }

    function reverseY(){
      if (sign_y==1){ 
        $("#y_pm").attr("src","static/images/minus_btn.png");
        sign_y = -1;
        console.log("sign_y = ",sign_y);
        return
      }
      if (sign_y==-1){ 
        $("#y_pm").attr("src","static/images/plus_btn.png");
        console.log("src = ","{{url_for('static', filename='images/plus_btn.png') }}");
        sign_y = 1;
        console.log("sign_y = ",sign_y);
        return
      }
    }


    function reverseZ(){
      if (sign_z==1){ 
        $("#z_pm").attr("src","static/images/minus_btn.png");
        sign_z = -1;
        console.log("sign_z = ",sign_z);
        return
      }
      if (sign_z==-1){ 
        $("#z_pm").attr("src","static/images/plus_btn.png");
        console.log("src = ","{{url_for('static', filename='images/plus_btn.png') }}");
        sign_z = 1;
        console.log("sign_z = ",sign_z);
        return
      }
    }

    function launchProbe(){

      const final_x = sign_x * x;
      const final_y = sign_y * y;
      const final_z = sign_z * z;

      $("#x_desto").val(final_x);
      $("#y_desto").val(final_y);
      $("#z_desto").val(final_z);

      console.log("Launching probe");
      return true;

    }
});