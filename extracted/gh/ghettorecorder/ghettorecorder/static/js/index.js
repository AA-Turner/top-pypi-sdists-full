/* Basic Browser Web audio interface with Python HTTP server to visualize and manipulate network sound.

  No JQuery in this project!
*/
const cl = console.log
var glob = undefined;  // catch error undefined if we are wrong
var hiddenOnOff = undefined;  // keep status of element display attribute

window.addEventListener('load', function() {
    /**
     * Html loaded, can get id and class now.
     */
    console.log('All assets are loaded');
    const audioR = document.getElementById('audioR');
    const gainR = document.getElementById('gainR');
    gainR.addEventListener("input", setAudioGain);  // move slider of gain
    setInterval(ajax_title_get, 10000);
    const canvasBalloon = document.getElementById('canvasBalloon');
    glob = new Glob()
    glob.updateScreen();
    hiddenOnOff = new HiddenOnOff()
    // Gather all elements in the draggable-div class into a collection
    let draggable = document.querySelectorAll(".draggable-div");
    draggable.forEach(function(el){
      dragElement(el);  // animate.js
      touchMoveMobile(el)  // animate.js
    });
})
;

class Glob{
  /* *
   * global variables container and base functions resort
   */
  constructor() {
    this.playingRadio = false; // (browser audio element) <- (http server method loop) <- (py instance.audio_out queue)
    this.waitShutdownIntervalId = 0;  // store id of setInterval to disable setInterval(ajax_wait_shutdown, 2500);
    this.animationRuns = 0;
    this.windowWidth = window.innerWidth;
  }
  numberRange (start, end) {  // simulate range() of Python
    return new Array(end - start).fill().map((d, i) => i + start);
  }
  // return a random integer
  getRandomIntInclusive(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }
  updateScreen() {
    // called by checkWindowWidth(); rearrange for mobiles small screens
    let divAirOne = document.getElementById('divAirOne');
    let spanHeaderCenter = document.getElementById('spanHeaderCenter');
    spanHeaderCenter
    if(this.windowWidth <= 1080) {
      divAirOne.style.top = "26em";
      divAirOne.style.left = "2.0em";
      spanHeaderCenter.innerHTML = "Ghetto";
    }else {
      divAirOne.style.top = "14em";
      divAirOne.style.left = "2.0em";
      spanHeaderCenter.innerHTML = "GhettoRecorder";
    }
  }
}
;

function checkWindowWidth() {
  glob.windowWidth = window.innerWidth;
  glob.updateScreen();
}
;
window.addEventListener('resize', checkWindowWidth);


class HiddenOnOff{
    /** End the miserable behavior of asking for display attribute and get back bullsh*t. Result in "must" double click.
     * Switch the visibility of an element on/off. Javascript has no Py getattr, setattr. We save elem names as key.
     * Overkill for one or two divs, but becomes handy for reuse.
     * Reading the display status leads often to switch pb. e.g. double click to hide. We save status in vars.
     * Use:
     *  init at the bottom of this script
     *  hiddenOnOff = new HiddenOnOff()
     *  hiddenOnOff.update({element:'divControllerSlider', set:false})
     *  hiddenOnOff.toggle({element:'divControllerSlider'})
     */
  constructor() {
    // initial div values if page is loaded
    this.isSwitchedOn = {};
    this.isSwitchedOn['divOverlay'] = false;  // remove page cover to enable audio element in browser
    this.isSwitchedOn['divEdit'] = false;  // show, hide div edit settings.ini
    this.isSwitchedOn['divControllerSlider'] = false;  // show, hide div edit volume and gain
    this.isSwitchedOn['divEditConfig'] = false;  // editor for settings.ini
    this.isSwitchedOn['divEditBlacklist'] = false;  // editor for blacklist.json
    this.isSwitchedOn['divBalloon'] = true;  // canvas balloon with basket

    // edit menu option p elements
    this.isSwitchedOn['pShutdown'] = true;
    this.isSwitchedOn['pDocu'] = true;
    this.isSwitchedOn['pEditConfig'] = true;
    this.isSwitchedOn['pEditBlacklist'] = true;

    // Airplane
    this.isSwitchedOn['svgAirOne'] = true;
  };
  update(options) {
    // set action explicit
    if(options === undefined) alert('HiddenOnOff update no options');  // just show how this options guy is working
    if(options.element === undefined) alert('HiddenOnOff update no element');
    let obj = document.getElementById(options.element);

    if (options.set) {
      obj.style.display = 'inline-block';
      this.isSwitchedOn[options.element] = true;
    } else {
      obj.style.display = 'none';
      this.isSwitchedOn[options.element] = false;
    }
  };
  toggle(options) {
    if(options.element === undefined) alert('HiddenOnOff update no element');
    let obj = document.getElementById(options.element);

    if (!this.isSwitchedOn[options.element]) {
      obj.style.display = 'inline-block';  // toggle
      this.isSwitchedOn[options.element] = true;  // toggle

      // switch on animation for airplane
      if(options.element == "svgAirOne") {
        animatedAirplane();
      }
    } else {
      obj.style.display = 'none';
      this.isSwitchedOn[options.element] = false;

      // switch off animation for airplane
      if(options.element == "svgAirOne") {
        cancelAnimation(animatedAirplaneKiller);
      }
    }
  };
}
;

function audioEnable () {
    /** in INDEX.HTML, overlay div click enables audio
     * User interaction required to enable audio context.

     * Switch on animations.
     */
    setAudioContextVisual();
    draw();  // animate.js
    enableAirplane();
}
;

function setAudioContextVisual() {
    /**
     * Create audio nodes and connect them.
     */
    audioContext = new AudioContext();  // instance IS same as audioR, but then we must use JS to apply controls
    gainNode = audioContext.createGain();
    analyserNode = audioContext.createAnalyser();
    audioSource = audioContext.createMediaElementSource(audioR);  // audioR elem defined in index.html to show controls
    // connect audio network client of index.html with analyser, with gain control and then with computer speaker
    audioSource.connect(analyserNode).connect(gainNode).connect(audioContext.destination);
}
;
function setAudioGain() {
    /**
     * Gain controller value input if slider in action.
     */
    gainNode.gain.value = gainR.value;
}
;
function ajax_switch_radio(radio_btn_id) {
    /**
     * AJAX - radio btn press start recorder and or audio element in browser.
     * radio_btn_id is actually the name of the radio,
     *   it has a minus before the name if it is removed (stop)
     */
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/radio_btn_id');

    xhr.onload = function () {
      console.log('xhr r ', xhr.response);
      var data = JSON.parse(xhr.responseText);
      console.log('resp r ', data.content);
      // response from stop request, dict all null, except radio_name is: -randio
      if (!data.radio_dir) {
        // set var for interval title scan
        glob.playingRadio = false;
      }
      /* radio buttons */
      let divRadioBtn=document.getElementsByClassName('divRadioBtn');
      // set all uniform
      for(var i = 0; i < divRadioBtn.length; i++){
        divRadioBtn[i].style.color = '#000000';
        divRadioBtn[i].style.backgroundColor = '#f9f9f9ff';
      }
      // adapt recorder active buttons
      for (const elem of data.recorder) {
        let rec=document.getElementById('div' + elem);
        rec.style.color='#f9f9f9ff';
        rec.style.backgroundColor='#fd7f7f';
      }
      /* bottom page footer */
      let pMsg=document.getElementById('pMsg');
      pMsg.innerHTML='';
      pMsg.innerHTML=xhr.response;
      pMsg.style.backgroundColor='#cf4d35ff';
      pMsg.style.fontFamily='PT Sans, arial';
      pMsg.style.padding='10px';pMsg.style.color='#f9f9f9ff';
      /* radio shall run but is not responding */
      if (data.content == "no_response") {
        console.log('no_response ', data.radio_name);
        let radio = document.getElementById("div" + data.radio_name);
        radio.style.backgroundColor='black';
        return;
      }
      /* enable sound */
      let audioR = document.getElementById('audioR');
      // stopped radio btn has (-) a minus in front of the name
      if (data.radio_name == radio_btn_id) {  // data.radio_name is ajax return value
          audioR.src='http://localhost:' + data.server_port + '/sound/' + data.radio_name;
          let playPromise = audioR.play();    // must check status, else DOM promise error in log
          if (playPromise !== undefined) {
            playPromise.then(function() {
              // "Automatic playback started!"
            }).catch(function(error) {
              // "Automatic playback failed."
            });
          }
        // set var for interval title scan
        glob.playingRadio = data.radio_name;
      }
    };
    xhr.send(radio_btn_id);
}
;
function ajax_title_get() {
    /**
     * AJAX - active radio title display.
     */
    console.log('glob.playingRadio ', glob.playingRadio);
    if (!glob.playingRadio) {return;}
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/title_get');

    xhr.onload = function () {
      var data = JSON.parse(xhr.responseText);
      console.log('resp t ', data.title);
      if (!data.title) {return;}
        let pTitle=document.getElementById('pTitle');
        pTitle.style.fontFamily='PT Sans, arial';pTitle.style.padding='10px';
        pTitle.innerHTML=''; pTitle.innerHTML= '[' + glob.playingRadio + '] ' + data.title;
    };
    xhr.send(glob.playingRadio);
}
;
function ajax_get_config_file() {
    /**
     * AJAX - settings.ini file in cheapo 'editor' mode.
     */
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/get_config_file');

    xhr.onload = function () {
      var data = JSON.parse(xhr.responseText);
      console.log('resp gc ', data);
      let configFileEdit = document.getElementById('configFileEdit');
      configFileEdit.value = data.get_config_file;
      // write path of file
      let configFileEditPath = document.getElementById('configFileEditPath');
      configFileEditPath.innerHTML = data.path;
      configFileEditPath.style.backgroundColor = '#fd7f7f';
    };
    xhr.send(null);
}
;
function ajax_write_config_file() {
    /**
     * AJAX - settings.ini file send back to file system.
     */
    let configFileEdit = document.getElementById('configFileEdit');
    var configContent = configFileEdit.value;

    const xhr = new XMLHttpRequest();
    
    xhr.open('POST', '/write_config_file');
    xhr.onload = function () {
      var data = JSON.parse(xhr.responseText);
      console.log('resp wc ', data.write_config_file);
      
      let pConfigResponse = document.getElementById('pConfigResponse');
      pConfigResponse.innerHTML= data.write_config_file;
    };
    xhr.send(configContent);
}
;
function ajax_get_blacklist_file() {
    /**
     * AJAX - blacklist.json file in cheapo 'editor' mode.
     */
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/get_blacklist_file');

    xhr.onload = function () {
      var data = JSON.parse(xhr.responseText);
      // console.log('resp gb ', data);
      let blacklistFileEdit = document.getElementById('blacklistFileEdit');
      blacklistFileEdit.value = data.get_blacklist_file;
      // write path of file
      let blacklistFileEditPath = document.getElementById('blacklistFileEditPath');
      blacklistFileEditPath.innerHTML = data.path;
      blacklistFileEditPath.style.backgroundColor = '#fd7f7f';
    };
    xhr.send(null);
}
;
function ajax_write_blacklist_file() {
    /**
     * AJAX - blacklist.json file send back to file system.
     */
    let blacklistFileEdit = document.getElementById('blacklistFileEdit');
    var blacklistContent = blacklistFileEdit.value;

    const xhr = new XMLHttpRequest();

    xhr.open('POST', '/write_blacklist_file');
    xhr.onload = function () {
      var data = JSON.parse(xhr.responseText);
      // console.log('resp wb ', data.write_blacklist_file);

      let pBlacklistResponse = document.getElementById('pBlacklistResponse');
      pBlacklistResponse.innerHTML= data.write_blacklist_file;
    };
    xhr.send(blacklistContent);
}
;
function ajax_server_shutdown() {
    /**
     * AJAX - recorder shut down via server call.
     */
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/server_shutdown');
    
    xhr.onload = function () {
      var data = JSON.parse(xhr.responseText);
      console.log('resp ss ', data.server_shutdown);

      let pMsg = document.getElementById('pMsg');
      let sMsgShutDown = document.getElementById('sMsgShutDown');
      pMsg.innerHTML = '';
      pMsg.innerHTML = data.server_shutdown;
      sMsgShutDown.style.backgroundColor = 'lightGreen';
      sMsgShutDown.innerHTML = data.server_shutdown;
      glob.waitShutdownIntervalId = setInterval(ajax_wait_shutdown, 2500);
    };
    xhr.send();
}
;
function ajax_wait_shutdown() {
    /**
     * AJAX - Show the current shut down status.
     */
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/wait_shutdown');
    xhr.timeout = 2000;
    
    xhr.onload = function () {
      var data = JSON.parse(xhr.responseText);
      console.log('resp ws ', data.wait_shutdown);

      let pMsg = document.getElementById('pMsg');
      let sMsgShutDown = document.getElementById('sMsgShutDown');

      pMsg.innerHTML = '';
      pMsg.innerHTML = data.wait_shutdown;
      sMsgShutDown.style.backgroundColor = 'lightYellow';
      sMsgShutDown.innerHTML = data.wait_shutdown;
    };
    xhr.ontimeout = function (e) {
      // request timed out
      pMsg.innerHTML = '';
      pMsg.innerHTML = 'down';

      sMsgShutDown.style.backgroundColor = '#fd7f7f';
      sMsgShutDown.innerHTML = '';
      sMsgShutDown.innerHTML = 'down';
      // disable setInterval
      clearInterval(glob.waitShutdownIntervalId);
    };
    xhr.send();
}
;
