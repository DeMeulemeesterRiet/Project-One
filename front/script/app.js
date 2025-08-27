'use strict';

const lanIP = `${window.location.hostname}:5000`;
// const lanIP = `192.168.168.169:5000`;

const socketio = io(lanIP);

// #region ***  DOM references                           ***********
let token = '';
let htmlinloggen;
// #endregion

// #region ***  Authentication                           ***********
const callbackError = function (data) {
  console.info(data);
};

const callbackShowToken = function (jsonObject) {
  console.info('callbackShowToken');
  console.log(jsonObject);
  // let htmlstring = '';
  document.querySelector('.js-user').value = '';
  document.querySelector('.js-password').value = '';

  // htmlstring += '<br>' + jsonObject.message;
  if (jsonObject.access_token) {
    token = jsonObject.access_token;
    localStorage.setItem('accessToken', token);
    // htmlstring += '<br/> Generated token is <b>' + token + '</b>';
    // window.location.href = `home.html`;
  
  }
  token = localStorage.getItem('accessToken');
  handleData(`http://${lanIP}/projectOne/RietDeMeulemeester/protected/`, callbackShowUser, callbackShowErrorNoToken, 'GET', null, token);
  // document.querySelector('.js-result').innerHTML += htmlstring;
  // let htmlstring2 = '';
  // htmlstring2 += `<a href="home.html"><div >Protected endpoint home</div></a>`;
  // document.querySelector('.js-result').innerHTML += htmlstring2;
};

const callbackShowUser = function (jsonObject) {
  // let htmlstring = '';
  // htmlstring += jsonObject.message;
  // if (jsonObject.logged_in_as) {
  //   htmlstring += 'Logged in with user <b>' + jsonObject.logged_in_as + '</b>';
  // }
  // document.querySelector('.js-result').innerHTML += htmlstring;
  // let htmlstring2 = '';
  // htmlstring2 += `<a href="home.html"><div >Protected endpoint home</div></a>`;
  // document.querySelector('.js-result').innerHTML += htmlstring2;
  window.location.href = `home.html`;
};

const callbackShowErrorNoToken = function (data) {
  console.info('callbackShowErrorNoToken');
  if (data.status === 422) {
    //422 = Er is geen token
    document.querySelector('.js-result').innerHTML = 'Gelieve eerst in te loggen.';
  }
  if (data.status === 401) {
    //401 = Token is niet meer geldig
    document.querySelector('.js-result').innerHTML = 'Ongeldige gebruikersnaam en/of wachtwoord.';
  }
  if (data.status === 449) {
    //401 = Token is niet meer geldig
    document.querySelector('.js-result').innerHTML = 'Gelieve gebruikersnaam en wachtwoord in te vullen.';
  }
};

const callbackShowErrorNoLogin = function (data) {
  console.info(data);
  if (data.status === 401) {
    //401 = Token is niet meer geldig
    document.querySelector('.js-result').innerHTML = `${data.statusText}`;
  }
};

// #endregion Authentication

// #region ***  Callback-Visualisation - show___         ***********
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********
// #endregion

// #region ***  Event Listeners - listenTo___            ***********

const loadUIEventListeners = function () {
  // Klikevent koppelen aan de GENERATE-knop
  document.querySelector('.js-button-generate').addEventListener('click', function () {
    console.log('generating....');
    const body = JSON.stringify({
      username: document.querySelector('.js-user').value,
      password: document.querySelector('.js-password').value,
    });
    handleData(`http://${lanIP}/projectOne/RietDeMeulemeester/login/`, callbackShowToken, callbackShowErrorNoToken, 'POST', body);
  });

  // document.querySelector('.js-button-reset').addEventListener('click', function () {
  //   token = null;
  //   localStorage.clear();
  //   document.querySelector('.js-result').innerHTML = 'Token gewist in frontend';
  // });

  // document.querySelector('.js-button-public').addEventListener('click', function () {
  //   handleData(`http://${lanIP}/projectOne/RietDeMeulemeester/public/`, callbackShowUser, callbackError, 'GET', null);
  // });

  // document.querySelector('.js-button-protected').addEventListener('click', function () {
  //   token = localStorage.getItem('accessToken');
  //   handleData(`http://${lanIP}/projectOne/RietDeMeulemeester/protected/`, callbackShowUser, callbackShowErrorNoToken, 'GET', null, token);
  // });
};


const listenToUI = function () {
  //niet vergeten functie aan te roepen in de init !!!!!!!
};

const listenToSocket = function () {
  //niet vergeten functie aan te roepen in de init !!!!!!!
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });
  socketio.on('disconnect', function () {
    console.log('verbinding verbroken met socket webserver');
    localStorage.clear();
  });

  socketio.on('B2F_home_tonen', function (msg) {
    window.location.href = `home.html`;
    socketio.emit('F2B_zijn_home', msg)
  });
};
// #endregion

// #region ***  Init / DOMContentLoaded                  ***********
const init = function () {
  console.info('DOM geladen');
  token = localStorage.getItem('accessToken');
  
  htmlinloggen = document.querySelector(`.js-inloggen`);
  
  if (htmlinloggen){
    loadUIEventListeners();
  }

  listenToUI();
  listenToSocket();
};

document.addEventListener('DOMContentLoaded', init);
// #endregion
