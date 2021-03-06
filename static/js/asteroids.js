
      const FPS = 30; // frames per second
      const SHIP_SIZE = 30; //ship height in pixels
      const ASTERS_JAG = 0.4; //jaggedness of asteroids 0 - 0.1
      const TURN_SPEED = 360; //turn speed in degrees per second
      const SHIP_THRUST = 5; //acceleration
      const FRICTION = 0.3;
      const ASTERS_NUM = 5; //default number of asteroids
      const ASTERS_SIZE = 100;
      const ASTERS_VERT = 10; //number of verticies of the asteroids
      const SHOW_CENTER_DOT = false;
      const LASER_SPD = 120;
      const LASER_MAX = 10;
      const LASER_SIZE = 12;
      const LASER_TIME = 110; //Number of frames before the laser disappears.
      const DIFFICULTY_RAMP = 0.2; //how quickly the level increases affect asteroid speed
      const ASTERS_INCREASE_INCREMENT = 5; //number of levels before a new asteroid is added to the belt
      const SCORE_INCREMENT = 10; //score +10 for every asteroid piece destroyed
      const NEW_LEVEL_COUNTDOWN = 40;
      const LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
      /** @type {HTMLCanvasElement} */
      var canv = document.getElementById("Screen");
      var ctx = canv.getContext("2d");
      //Event Handelers
      document.addEventListener("keydown", keyDown);
      document.addEventListener("keyup", keyUp);
      //set up game loop
      setInterval(update, 1000 / FPS);
      //Initial Variables
      var level = 1;
      var score = 0; //score +SCORE_INCREMENT for every asteroid piece destroyed
      var server_score = 0;
      var asters_speed = 30; //determines speed for asteroids
      var explode_time = 0;
      var dead_ship = false;
      var game_end_counter = 0;
      var new_level_countdown = NEW_LEVEL_COUNTDOWN;
      //highscore variables
      var got_highscore = false;
      var initials = ["A", "A", "A"];
      var score_cursor = 0;
      var score_letter_index = 0;
      var added_counter = 0; //loop counter to desplay that score was sent to server
      var bad = false;
      //Initialize new ship
      var ship = {
            x: canv.width / 2,
            y: canv.height / 2,
            r: SHIP_SIZE / 2,
            a: 90 / 180 * Math.PI, // convert to radians
            rot: 0,
            thrust: false,
            loaded: true, //able to shoot a laser
            lasers: [],
            speed: {
              x: 0,
              y: 0,
            }
          }
      // set up ASTEROIDS
      var asters = [];
      function Initialize_Game(){
        // level,score, asters_speed, explode_time, dead_ship, game_end_counter, new_level_countdown, ship, asters
        return Initial_Values_List = [1, 0 ,30 ,0 ,false ,0 ,NEW_LEVEL_COUNTDOWN, {x: canv.width / 2, y: canv.height / 2, r: SHIP_SIZE / 2, a: 90 / 180 * Math.PI, rot: 0, thrust: false, loaded: true, lasers: [], speed: {x: 0, y: 0,}},[]] //Resetting the IVL resets the game.
        }
      function Laserfire() {
        if (ship.loaded == true && ship.lasers.length < LASER_MAX){
            ship.lasers.push({ // from the nose of the ship
              x: ship.x + 4 / 3 * ship.r * Math.cos(ship.a),
              y: ship.y - 4 / 3 * ship.r * Math.sin(ship.a),
              xv: LASER_SPD * Math.cos(ship.a) / FPS,
              yv: -LASER_SPD * Math.sin(ship.a) / FPS,
              time: LASER_TIME
            });
        }
        //create laser
        ship.canShoot = false;
      }
      function distBetweenPoints (x1, y1, x2, y2) {
        distance = Math.sqrt((x2- x1)**2 + (y1- y2)**2);
        return distance;
        }
    function explodeShip(time) { //used when game ends
        ctx.fillStyle = "red";
        ctx.beginPath();
        ctx.arc(ship.x, ship.y, time, 0, Math.PI*2);
        ctx.closePath();
        ctx.fill();
    }
      function createAsteroidBelt(level) {
          asters = [];
          var x, y;
          for(var i = 0; i < ASTERS_NUM + Math.floor(level/ASTERS_INCREASE_INCREMENT); i++){ //one new asteroid every 10 levels
            do {
              x = Math.floor(Math.random() * canv.width);
              y = Math.floor(Math.random() * canv.height);
            } while (distBetweenPoints(ship.x, ship.y, x, y) < ASTERS_SIZE*2 + ship.r);
            asters.push(newAsteroid(x, y, 3, level)); //class 3 'starting' asteroid
          }
      }
      function keyDown(/** @type {KeyboardEvent} */ ev) {
        switch(ev.keyCode){
          case 32: //space bar
              Laserfire();
              break;
          case 37: //left arrow
              ship.rot = TURN_SPEED / 180 * Math.PI / FPS;
              if(got_highscore == true){
                  if (score_cursor > 0){
                    score_cursor -= 1;
                    for(i=0; i<25; i++){
                      if (initials[score_cursor] === LETTERS.charAt(i)){
                          score_letter_index = i;
                      }
                    }
                  }
              }
              break;
          case 38: // up
              ship.thrust = true;
              if(got_highscore == true){
                  if(score_letter_index < 24){
                    score_letter_index += 1;
                  }else{
                    score_letter_index = 0;
                  }
              }
              break;
          case 39: // right arrow
              ship.rot = -TURN_SPEED / 180 * Math.PI / FPS;
                if(got_highscore == true){
                  if (score_cursor < 2){
                    score_cursor += 1;
                    for(i=0; i<25; i++){
                          if (initials[score_cursor] === LETTERS.charAt(i)){
                              score_letter_index = i;
                            }
                          }
                    }
                }
              break;
          case 40: //down arrow
              if(got_highscore == true){
                if(score_letter_index < 1){
                  score_letter_index = 24;
                } else{
                  score_letter_index -= 1;
                }
              }
              break;
          case 13: //Enter
          if (got_highscore == true){
            if(initials[0]+initials[1]+initials[2] === "ASS" ||
            initials[0]+initials[1]+initials[2] === "GAY" ||
            initials[0]+initials[1]+initials[2] === "FAG" ||
            initials[0]+initials[1]+initials[2] === "NIG"){
              bad = true;
            } else{
              got_highscore = false;
              var dict = {}
              dict["initials"] = initials[0]+initials[1]+initials[2];
              dict["value"] = String(score);
              dict["test"] =  9000;
              $.ajax({
                url: $SCRIPT_ROOT + "/post_score",
                type: "POST",
                contentType: 'application/json;charset=UTF-8',
                dataType: 'json',
                data: JSON.stringify(dict),
                success: function(data) {
                      if (data.score_added){
                        added_counter = 80;
                        score = initial_values[1];
                      }
                    }
              });
            }
              break;
          }
        }
      }
      function keyUp(/** @type {KeyboardEvent} */ ev) {
        switch(ev.keyCode){
          case 32: //space bar laser
                //prevent scrolling
                window.onscroll = function () { window.scrollTo(0, 0); };
              break;
          case 37: //left arrow
              ship.rot = 0;
              break;
          case 38: // up
              ship.thrust = false;
              break;
          case 39: // right arrow
              ship.rot = 0;
              break;
          }
      }
      function newAsteroid(x, y, designation, level) {
        var aster = {
          x: x,
          y: y,
          xv: ((Math.random()*((1/designation)+2/3) * asters_speed) + (((level - 1) * DIFFICULTY_RAMP) * asters_speed)) / FPS * (Math.random() < 0.5 ? 1: -1),
          yv: ((Math.random()*((1/designation)+2/3) * asters_speed) + (((level - 1) * DIFFICULTY_RAMP) * asters_speed)) / FPS * (Math.random() < 0.5 ? 1: -1),
          r: (ASTERS_SIZE*designation*2 + ASTERS_SIZE)/8,
          a: Math.random() * Math.PI * 2,
          vert: Math.floor(Math.random() * (ASTERS_VERT + 1) + ASTERS_VERT / 2),  //A random number between 5 and 15.
          tier: designation, //tier 3, 2, or 1
          offs: []
        };
        // create the vertex offets array
        for (var i = 0; i < aster.vert; i++) {
          aster.offs.push(Math.random() * ASTERS_JAG * 2 + 1 - ASTERS_JAG); //random between 0.5 - 1.5
        }
        return aster;
      }
      function destroyAsteroid(index, tier){
        var x = asters[index].x
        var y = asters[index].y
        var tier = asters[index].tier
        if(tier > 1){ //tier3, tier2 case
          asters.push(newAsteroid(x, y, tier - 1, level));
          asters.push(newAsteroid(x, y, tier - 1, level));
        } //else do nothing
        asters.splice(index, 1);
        score += SCORE_INCREMENT;
      }
        function update() {  // ---------------------------------------UPDATE LOOP!!!!-------------------------------
            //draw space
            ctx.fillStyle = "black"; //default color
            ctx.fillRect(0, 0, canv.width, canv.height); //origin (x,y), canvas width and height
            if(got_highscore == true){ // enter highscore loop
              ctx.font = "50px Arial";
              ctx.fillStyle = "blue";
              ctx.fillText(initials[0], canv.width/4, canv.height/2 - 50);
              ctx.fillText(initials[1], canv.width/4 + 50 , canv.height/2 - 50);
              ctx.fillText(initials[2], canv.width/4 + 100, canv.height/2 - 50);
              ctx.fillStyle = "green";
              if (score_cursor == 0){
                ctx.fillText(initials[score_cursor], canv.width/4, canv.height/2 - 50);
              }
              if (score_cursor == 1){
                ctx.fillText(initials[score_cursor], canv.width/4 + 50 , canv.height/2 - 50);
              }
              if (score_cursor == 2){
                ctx.fillText(initials[score_cursor], canv.width/4 + 100, canv.height/2 - 50);
              }
              ctx.fillStyle = "white";
              ctx.fillText("Your score was: " + String(score), canv.width/4 - 50, 100);
              ctx.font = "30px Arial";
              ctx.fillText("You got a high score! Enter your initials!", canv.width/4 -60, canv.height/2);
              ctx.font = "20px Arial";
              ctx.fillText("Press Arrows to select letters.", canv.width/4, canv.height-50);
              ctx.fillText("Press Enter to quit and save", canv.width/4, canv.height-10);
              if(bad){
                ctx.font = "50px Arial";
                ctx.fillStyle = "red";
                ctx.fillText("Do be tasteful", canv.width/4, canv.height-200);
              }
              initials[score_cursor] = LETTERS.charAt(score_letter_index);
            }
            else{ //          -------------DO EVERYTHING ELSE!!!--------------
              //  ------------------SERIOUSLY!!!!!!!!---------------------
              //NEW LEVEL POTENTIAL
              if (asters.length < 1){ //player eleiminated all the asteroids
                new_level_countdown -= 1;
                ctx.font = "50px Arial";
                ctx.fillStyle = "white";
                ctx.textAllign = "center";
                ctx.fillText("Level " + String(level), 10, 50);
                if (new_level_countdown < 1){
                  level += 1;
                  createAsteroidBelt(level);
                  ship.lasers = [];
                  new_level_countdown = NEW_LEVEL_COUNTDOWN;
                }
              }
            if(dead_ship == false){
              //draw fire
              if(ship.thrust){
                ctx.fillStyle = "white";
                ctx.strokeStyle = "blue";
                ctx.lineWidth = SHIP_SIZE / 10;
                ctx.beginPath();
                ctx.moveTo( //rear left
                ship.x - ship.r * (2 / 3 * Math.cos(ship.a) + 0.4*Math.sin(ship.a)),
                ship.y + ship.r * (2 / 3 * Math.sin(ship.a) - 0.4*Math.cos(ship.a))
                );
                ctx.lineTo( //rear center
                  ship.x - ship.r * (5 / 3 * Math.cos(ship.a)),
                  ship.y + ship.r * (5 / 3 * Math.sin(ship.a))
                );
                ctx.lineTo( //rear right
                  ship.x - ship.r * ( 2 / 3 * Math.cos(ship.a) - 0.4*Math.sin(ship.a)),
                  ship.y + ship.r * ( 2 / 3 * Math.sin(ship.a) + 0.4*Math.cos(ship.a))
                );
                ctx.closePath();
                ctx.fill();
                ctx.stroke();
              }
              //draw ship
              ctx.strokeStyle = "grey";
              ctx.fillStyle = "grey";
              ctx.lineWidth = SHIP_SIZE / 10;
              ctx.beginPath();
              ctx.moveTo(
                  ship.x + 4 / 3 * ship.r * Math.cos(ship.a),
                  ship.y - 4 / 3 * ship.r * Math.sin(ship.a)
              );
              ctx.lineTo( //rear left
                  ship.x - ship.r * (2 / 3 * Math.cos(ship.a) + Math.sin(ship.a)),
                  ship.y + ship.r * (2 / 3 * Math.sin(ship.a) - Math.cos(ship.a))
                  );
              ctx.lineTo( //rear right
                  ship.x - ship.r * ( 2 / 3 * Math.cos(ship.a) - Math.sin(ship.a)),
                  ship.y + ship.r * ( 2 / 3 * Math.sin(ship.a) + Math.cos(ship.a))
                  );
              ctx.closePath();
              ctx.fill();
              ctx.stroke();
              if (SHOW_CENTER_DOT){ //center dot of ship
                ctx.fillStyle = "white";
                ctx.fillRect(ship.x - 2, ship.y - 2, 4, 4); //2 pixels wide
              }
              //rotate ship
              ship.a += ship.rot;
              //move ship
              if (ship.thrust) {
                ship.speed.x += SHIP_THRUST*Math.cos(ship.a) / FPS;
                ship.speed.y += SHIP_THRUST*Math.sin(ship.a) / FPS;
              } else {
                ship.speed.x -= FRICTION*ship.speed.x / FPS;
                ship.speed.y -= FRICTION*ship.speed.y / FPS;
              }
              ship.x += ship.speed.x,
              ship.y -= ship.speed.y
          }
          //draw lasers
          for (var i = 0; i < ship.lasers.length; i++) {
                    ctx.fillStyle = "salmon";
                    ctx.beginPath();
                    ctx.arc(ship.lasers[i].x, ship.lasers[i].y, SHIP_SIZE / 15, 0, Math.PI * 2, false);
                    ctx.fill();
                }
            //handle lasers
            for (i=0;i < ship.lasers.length; i++ ){
              //degrade laser
              ship.lasers[i].time -= 1;
              if(ship.lasers[i].time < 0) {
                ship.lasers.splice(i, 1)
                continue;
                }
              //move lasers
              ship.lasers[i].x += ship.lasers[i].xv;
              ship.lasers[i].y += ship.lasers[i].yv;
              //hit scan ASTEROIDS
              var ax, ay, ar, lx, ly;
              lx = ship.lasers[i].x;
              ly = ship.lasers[i].y;
              for (var j=0; j < asters.length; j++) {
                ax = asters[j].x;
                ay = asters[j].y;
                ar = asters[j].r;
                if(distBetweenPoints(ax, ay, lx, ly) < ar){
                  destroyAsteroid(j);
                  ship.lasers.splice(i, 1);
                }
              }
              //edge of Screen
              if (ship.lasers[i].x < 0) {
                  ship.lasers[i].x = canv.width;
              }
              if (ship.lasers[i].x > canv.width) {
                  ship.lasers[i].x = 0;
              }
              if (ship.lasers[i].y < 0) {
                  ship.lasers[i].y = canv.height;
              }
              if (ship.lasers[i].y > canv.height) {
                  ship.lasers[i].y = 0;
                }
            }
              //draww the ASTEROIDS
              ctx.strokeStyle = "slategrey";
              ctx.fillStyle = "slategrey";
              ctx.linewidth = SHIP_SIZE / 20;
              var a, r, x, y, vert, offs;
              for (var i = 0; i < asters.length; i++){
                //get properties
                x = asters[i].x;
                y = asters[i].y;
                r = asters[i].r;
                a = asters[i].a;
                vert = asters[i].vert;
                offs = asters[i].offs;
                //draw asteroid
                ctx.beginPath();
                ctx.moveTo(
                  x + r * offs[0] * Math.cos(a),
                  y - r * offs[0] * Math.sin(a)
                );
                    for (var j = 1; j < vert; j++){
                      ctx.lineTo(
                        x + r * offs[j] * Math.cos(a + j * Math.PI * 2 / vert),
                        y - r * offs[j] * Math.sin(a + j * Math.PI * 2 / vert)
                      );
                  }
                ctx.closePath();
                ctx.stroke();
                //move the asteroids
                asters[i].x += asters[i].xv
                asters[i].y += asters[i].yv
                //handle edge of screen
                if (asters[i].x < 0 - asters[i].r) {
                    asters[i].x = canv.width + asters[i].r;
                }
                if (asters[i].x > canv.width + asters[i].r) {
                    asters[i].x = 0 - asters[i].r;
                }
                if (asters[i].y < 0 - asters[i].r) {
                    asters[i].y = canv.height + asters[i].r;
                }
                if (asters[i].y > canv.height + asters[i].r) {
                    asters[i].y = 0 - asters[i].r;
                  }
            }
           //wrap screen
           if (ship.x < 0 - ship.r) {
               ship.x = canv.width + ship.r;
           }
           if (ship.x > canv.width + ship.r) {
               ship.x = 0 - ship.r;
           }
           if (ship.y < 0 - ship.r) {
               ship.y = canv.height + ship.r;
           }
           if (ship.y > canv.height + ship.r) {
               ship.y = 0 - ship.r;
           }
           //display score
           ctx.font = "20px Arial";
           ctx.fillStyle = "white";
           ctx.fillText("Score: " + String(score) + "  ", canv.width - 150, 50);
           if(added_counter > 0){
             ctx.fillStyle = "green";
             ctx.fillText("Highscore Uploaded!!", canv.width - 250, 90);
             added_counter -= 1;
         }
           //Kill Ship!
           for(var i = 0; i < asters.length; i++) {
              if (distBetweenPoints(asters[i].x, asters[i].y, ship.x, ship.y) < asters[i].r + ship.r || dead_ship == true){
                explode_time += 5;
                explodeShip(explode_time);
                dead_ship = true;
                ctx.font = "50px Arial";
                ctx.fillStyle = "white";
                ctx.fillText("GAME OVER x_x", canv.width/4 , canv.height/2); //divide by 4 works??
                game_end_counter += 1;
              }
            }
            if (game_end_counter > 180){
              // level, score, asters_speed, explode_time, dead_ship, game_end_counter, new_level_countdown, ship, asters
              $.ajax({
                url: $SCRIPT_ROOT + "/get_tenth",
                type: "GET",
                success: function(data) {
                    server_score = data.tenth_place
                    if(data.tenth_place < score){
                        got_highscore = true;
                       }
                    else{
                        score = initial_values[1];
                       }
                    }
               });
              initial_values = Initialize_Game();
              level = initial_values[0];
              asters_speed = initial_values[2];
              explode_time = initial_values[3];
              dead_ship = initial_values[4];
              game_end_counter = initial_values[5];
              new_level_countdown = initial_values[6];
              ship = initial_values[7];
              asters = initial_values[8];
              dead_ship = false;
             };
        } //DO EVERYTHING ELSE BRACKET!!!
      };