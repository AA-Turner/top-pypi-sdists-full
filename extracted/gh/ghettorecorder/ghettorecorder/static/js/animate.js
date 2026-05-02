function cancelAnimation(killerVar) {
    /**
     * Killer shall be an internal id of requestAnim......
     * Must be done, else we have overlay of several animations on canvas.
     */
      try {
        window.cancelAnimationFrame(killerVar);
      } catch (error) { console.error(error); }
}
;
function callAnimation() {
    /**
     * Switch for two analyzer functions.
     */
    if (glob.animationRuns == 0) {
      cancelAnimation(drawKiller);
      animatedBars();
      glob.animationRuns = 1;
    } else {
      cancelAnimation(animatedBarsKiller);
      draw();
      glob.animationRuns = 0;
    }
}
;
function draw() {
    /**
     * Jumping horizontal lines.
     */
    canvas = document.getElementById('canvasBalloon');
    canvasCtx = canvas.getContext('2d');
    analyserNode.fftSize = 2048;
    const bufferLength = analyserNode.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    analyserNode.getByteTimeDomainData(dataArray);

    canvasCtx.clearRect(0, 0, canvas.width, canvas.height); // not if second anim in background
    canvasCtx.lineWidth = 2.0;

    const gradient = canvasCtx.createLinearGradient(canvas.width/1.5, 0, canvas.width/2, canvas.height);
    gradient.addColorStop(0, "lightYellow");
    gradient.addColorStop(1, "turquoise");
    canvasCtx.fillStyle = gradient; //'turquoise';

    canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
    canvasCtx.strokeStyle = 'red';canvasCtx.beginPath();
    var sliceWidth = canvas.width * 1.0 / bufferLength;var x = 0;
    for (var i = 0; i < bufferLength; i++) {var v = dataArray[i] / 128.0;
      var y = v * canvas.height / 2;
      if (i === 0) {canvasCtx.moveTo(x, y);} else {canvasCtx.lineTo(x, y);}
      x += sliceWidth;}
    canvasCtx.stroke();

    drawKiller = window.requestAnimationFrame(draw);
}
;
function animatedBars() {
    /**
     * Vintage equalizer style.
     */
    canvas = document.getElementById('canvasBalloon');
    canvasCtx = canvas.getContext('2d');
    analyserNode.fftSize = 128;
    const bufferLength = analyserNode.frequencyBinCount;
    var barWidth = (canvas.width / bufferLength) * 2;
    const dataArray = new Uint8Array(bufferLength);
    analyserNode.getByteFrequencyData(dataArray);
    x = 0 - barWidth * 2;
    canvasCtx.clearRect(0, 0, canvas.width, canvas.height);  // not if second anim in background

 for (let i = 0; i < bufferLength; i++) {
    barHeight = ((dataArray[i]/2) - 12) + 2;
    canvasCtx.lineWidth = 3;
    canvasCtx.fillStyle = 'red';
    canvasCtx.fillRect(x, canvas.height - barHeight - 3, barWidth, 3);
    canvasCtx.fillStyle = 'rgb(219, 111, 52)';
    canvasCtx.fillRect(x, canvas.height - barHeight - 6, barWidth, 3);
    canvasCtx.fillStyle = 'blue';
    canvasCtx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
    x += barWidth;
}
  animatedBarsKiller = window.requestAnimationFrame(animatedBars);
}
;
function enableAirplane() {
  /* audioEnable() call us on start */
    // colorize plane
    doubleDecker = new FourShadesSVG( {svgGroup:"#gAirOne"} );
    doubleDecker.pathListsGet();
    doubleDecker.colorPaletteGet();
    doubleDecker.colorPalettePush();
    // colorize pilot just for fun, red baron?
    document.getElementById("airOne_pilotTwo_neck").style.fill = "#CC1100";
    document.getElementById("airOne_pilotTwo_scarfOne").style.fill = "#CC1100";
    document.getElementById("airOne_pilotTwo_scarfTwo").style.fill = "#CC1100";
    document.getElementById("airOne_pilotTwo_scarfThree").style.fill = "#CC1100";
    document.getElementById("airOne_pilotTwo_scarfFour").style.fill = "red";
    // show hide elements
    gPropNose = new ShowHideElemGroups({pathList: "#gPropNose"});
    gPropAxis = new ShowHideElemGroups({pathList: "#gPropAxis"});
    gScarfGroup = new ShowHideElemGroups({pathList: "#gScarfGroup"});
    gPropReflect = new ShowHideElemGroups({pathList: "#gPropReflect"});
    // requestAnimationFrame
    animatedAirplane();
}
;
function animatedAirplane() {
    // requestAnimationFrame needs a var to kill animation, upstairs - cancelAnimation(animatedAirplaneKiller);
    animatedAirplaneKiller = window.requestAnimationFrame(animatedAirplane);

    if (hiddenOnOff.isSwitchedOn["svgAirOne"]) {  // called onClick on div element in index.html
      // movement show; here we can optimize to get a perfect imagination, but who cares about the ghetto
      if(animatedAirplaneKiller % 11 == 0) {  // mobile CPU need a rest, but anim will suffer
          gScarfGroup.update();  // created in enableAirplane()
          gPropReflect.update();
      }
      if(animatedAirplaneKiller % 66 == 0) {
          gPropNose.update();
      }
      if(animatedAirplaneKiller % 123 == 0) {
          gPropAxis.update();
      }
      // plane color
      if(animatedAirplaneKiller % 543 == 0) {  // 60 frames per second; 10 sec calc new color plus shades
        this.doubleDecker = new FourShadesSVG( {svgGroup:"#gAirOne"} );
        this.doubleDecker.pathListsGet();
        this.doubleDecker.colorPaletteGet();
        this.doubleDecker.colorPalettePush();
      }
    }
}
;

class ShowHideElemGroups {
  /* Enable to show, hide multiple DOM element groups at once.

   Store current index of element in path list switched.
   myGroup = new ShowHideElemGroups( {pathList: "#gScarfGroup"}) ; path string is attached in constructor
   */
   constructor(opt) {
     this.pathsListArray = document.querySelectorAll(opt.pathList + " path");  // a collection object
     this.pathIndex = 0;
     this.pathList = [];  // clean list
     this.pathListGet();
   }
  pathListGet() {
    for(let index = 0; index <= this.pathsListArray.length -1; index++){  // pathsListArray (s) class FourShadesSVG
      let pID = this.pathsListArray[index].id;  // collection .id
     this.pathList.push(pID);
    }
  }
  update() {
    for(let index = 0; index <= this.pathList.length - 1; index++) {
      let svgPath = document.getElementById(this.pathList[index]);

      if (index == this.pathIndex || (index - 1 < this.pathIndex && index > this.pathIndex + 1)) {
        svgPath.style.visibility = "hidden";
      } else {
        svgPath.style.visibility = "visible";
      }
    }

    this.pathIndex += 1;
    if(this.pathIndex > this.pathList.length -1) {
      this.pathIndex = 0
    }
    // cl(opt.index)
  }
}

class FourShadesSVG {
  /* Our desired SVG is constructed with four greyscale colored paths (names).
    It is the name that counts here.
    We use one nice base color and shade the grey colors in four steps.
    <path id="airOne_greyTwo_wing_tail"  , search "greyTwo"
    console.log(document.querySelectorAll("#gSvgSpeakerFlatWaves path")[0].id);

    glob.propReflect = new FourShadesSVG( {svgGroup:"#gPropReflect"} ); //
    glob.propReflect.pathListsGet();
   */
  constructor(options){
    this.forbiddenColors = glob.numberRange(215, 275);  // glob utility class at index.js
    this.pathsListArray = document.querySelectorAll(options.svgGroup + " path");  // options done "#gAirOne path"
    this.pathList = [];
    this.greyOnePathList = [];
    this.greyTwoPathList = [];
    this.greyThreePathList = [];
    this.greyFourPathList = [];
    this.greyLists = [this.greyOnePathList, this.greyTwoPathList, this.greyThreePathList, this.greyFourPathList];
    this.hslOne = null;
    this.hslTwo = null;
    this.hslThree = null;
    this.hslFour = null;
    this.hslInterpolationList = [];
  }

  pathListsGet() {
    /* SVG path names must match the grey keyword.
       I used to colorize the original image in grey colors.
       Gentler for the eyes in the long run. */
    for(let index = 0; index <= this.pathsListArray.length -1; index++){
      let pID = this.pathsListArray[index].id;
     this.pathList.push(pID);

     if (pID.includes("greyOne")) this.greyOnePathList.push(pID)
     if (pID.includes("greyTwo")) this.greyTwoPathList.push(pID)
     if (pID.includes("greyThree")) this.greyThreePathList.push(pID)
     if (pID.includes("greyFour")) this.greyFourPathList.push(pID)
    }
  }

  colorPaletteGet(force_hueNum) {
    /* Create random color. Work only with light part of hsl, like a photograph.
       Assign start and end for interpolation of four color shades.
       https://hypejunction.github.io/color-wizard/ to get an impression what is running here.
     */
     let hueNum = force_hueNum;
     if(!force_hueNum) {
       hueNum = glob.getRandomIntInclusive(0,360);
       while (true) {
         if(this.forbiddenColors.includes(hueNum)) {
           hueNum = glob.getRandomIntInclusive(0,360);
         } else {
            break;
          }
       }
     }
     let col = hueNum;
     let sat = 80;
     let light = 35;
     let step = 4;

     this.hslOne = "hsl(" + hueNum + "," + sat + "%," + light + "%)";  // hsl(339, 80%, 94%)
     this.hslTwo = "hsl(" + hueNum + "," + sat + "%," + (light += step * 1) + "%)";
     this.hslThree = "hsl(" + hueNum + "," + sat + "%," + (light += step * 2) + "%)";
     this.hslFour = "hsl(" + hueNum + "," + sat + "%," + (light += step * 3) + "%)";
     this.hslInterpolationList = [this.hslOne, this.hslTwo, this.hslThree, this.hslFour];
  }

  colorPalettePush() {
    /* Assign the color to the list of paths.
     */
    for(let index = 0; index <= this.greyLists.length -1; index++){
      let greyShad = this.greyLists[index];

      for(let kIndex = 0; kIndex <= greyShad.length -1; kIndex++) {
        let svgPathElem = document.getElementById(greyShad[kIndex]);
        svgPathElem.style.fill = this.hslInterpolationList[index];
      }
    }
  }
}
;

function dragElement(elem) {
/* div draggable */
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById(elem.id)) {
    // can be a touch bar to handle the div, other div id:
    document.getElementById(elem.id).onmousedown = dragMouseDown;
  } else {
    // otherwise move the div from elsewhere on div body
    elem.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // assign new coordinates based on the touch on the viewport .clientX
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position
    elem.style.top = (elem.offsetTop - pos2) + "px";
    elem.style.left = (elem.offsetLeft - pos1) + "px";
  }

  function closeDragElement() {
    // stop moving when mouse button is released
    document.onmouseup = null;
    document.onmousemove = null;
  }
}
;
function touchMoveMobile(box) {

  box.addEventListener('touchmove', function(e) {
    // grab the location of touch
    var touchLocation = e.targetTouches[0];

    // assign box new coordinates based on the touch.
    box.style.left = touchLocation.pageX + 'px';
    box.style.top = touchLocation.pageY + 'px';
  })

  /* record the position of the touch
  when released using touchend event.
  This will be the drop position. */

  box.addEventListener('touchend', function(e) {
    // current box position.
    var x = parseInt(box.style.left);
    var y = parseInt(box.style.top);
  })
}
;