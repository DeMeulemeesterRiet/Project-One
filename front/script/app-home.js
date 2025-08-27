'use strict';

let token = '';
const lanIP = `${window.location.hostname}:5000`;
// const lanIP = `192.168.168.169:5000`;

const socketio = io(lanIP);

// #region ***  DOM references                           ***********
let htmlgrafiek,htmlinloggen,htmlhome,htmlgebruiker;
let chart;
let html_wachtwoord, html_chatbox, html_button, html_naam;
let leerling_info
// #endregion

// #region ***  Callback-Visualisation - show___         ***********
const showWelkom = function(){
  try{
    token = localStorage.getItem('accessToken');
    let htmlstring = '';
    htmlstring += `<p class="js-gebruiker" data-leerling-naam="${token}"  data-leerlingid="${token}" >Welkom ${token}</p>`;
    document.querySelector('.js-welkom').innerHTML += htmlstring;    
  } catch (error) {
    console.error(error)
  }
};

const showOefensessies = function(obj){
  try{
    // console.info(obj)
    let htmlstring = '';
    for(let item of obj.records){
      htmlstring += `<tr class="c-row c-row__oefensessie js-oefensessie" data-oefensessieid="${item['oefensessieid']}" >
            <td>${item['startdatum']}</td>
            <td>${item['startuur']}</td>
            <td>Tafel ${item['getal1']}</td>
            <td>${item['aantal_correct']}/${item['totaal_aantal_oefeningen']}</td>
          </tr>`;
    }
    document.querySelector('.js-oefensessies').innerHTML = htmlstring; 
    listenToClickOefensessie()
  } catch (error) {
    console.error(error)
  }
};

const showErrorOefensessies = function (err) {
  console.info('in de error van tonen oefensessies');
  console.error(err);
};


const showOefensessieInfo = function(obj){
  try{
    // console.info(obj)
    let htmlstring = '';
    for(let item of obj.records){
      htmlstring += `<p>${item['startdatum']}</p>
                <p>${item['startuur']}</p>
                <p>Tafel ${item['getal1']}</p>
                <p>${item['aantal_correct']}/${item['totaal_aantal_oefeningen']}</p>`;
    }
    
    // document.querySelector('.js-oefeningen-info').innerHTML = htmlstring; 
    for (const oefeningendeel of document.querySelectorAll('.js-oefeningen-info')) {
      // console.log(oefeningendeel.innerHTML)
      oefeningendeel.innerHTML = htmlstring}
  } catch (error) {
    console.error(error)
  }
};

const showErrorOefensessieInfo = function (err) {
  console.info('in de error van tonen oefensessie info');
  console.error(err);
};


const showInfoLeerling = function(obj){
  try{
    // token = localStorage.getItem('accessToken');
    let htmlstring = '';
    htmlstring += `<p class="u-welkom-naam js-gebruiker" data-leerling-naam="${obj.info['naam']}"  data-leerlingid="${obj.info['leerlingid']}">Welkom ${obj.info['naam']}</p><p class="u-welkom-terug">Welkom terug!</p>`;
    document.querySelector('.js-welkom').innerHTML = htmlstring;        
  } catch (error) {
    console.error(error)
  }
};

const showErrorInfoLeerling = function (err) {
  console.info('in de error van tonen info leerling');
  console.error(err);
};


const showAantalOefensessiesLeerling = function(obj){
  try{
    // token = localStorage.getItem('accessToken');
    let htmlstring = '';
    htmlstring += `<p class="u-infoblok-getal"> ${obj.aantal['totaal_aantal_oefensessies']} </p>   <p class="u-infoblok-tekst"> keer geoefend</p>`;
    document.querySelector('.js-aantal-oefensessies').innerHTML = htmlstring;        
  } catch (error) {
    console.error(error)
  }
};

const showErrorAantalOefensessiesLeerling = function (err) {
  console.info('in de error van tonen aantal oefensessies leerling');
  console.error(err);
};


const showAantalOefeningenLeerling = function(obj){
  try{
    // token = localStorage.getItem('accessToken');
    let htmlstring = '';
    htmlstring += `<p class="u-infoblok-getal"> ${obj.aantal['totaal_aantal_oefeningen']} </p> <p class="u-infoblok-tekst"> oefeningen gemaakt</p>`;
    document.querySelector('.js-aantal-oefeningen').innerHTML = htmlstring;        
  } catch (error) {
    console.error(error)
  }
};

const showErrorAantalOefeningenLeerling = function (err) {
  console.info('in de error van tonen aantal oefensessies leerling');
  console.error(err);
};


const showOefeningenOefesessie = function(obj){
  try{
    // console.info(obj)
    let htmlstring = '';
    for(let item of obj.records){
      let kleur;
      if(item['correct'] == 1){
        kleur = 'c-row__oefening--juist'
      }
      else{
        kleur = 'c-row__oefening--fout'
      }
      htmlstring += `<tr class="c-row c-row__oefening ${kleur}">
        <td>${item['getal1']}</td>
        <td>x</td>
        <td>${item['getal2']}</td>
        <td>=</td>
        <td>${item['getal1'] * item['getal2']}</td>
        <td>${item['antwoord']}</td>
      </tr>`;
    }
    // document.querySelector('.js-oefeningen').innerHTML += htmlstring;   
    for (const oefeningendeel of document.querySelectorAll('.js-oefeningen')) {
      oefeningendeel.innerHTML = htmlstring}

  } catch (error) {
    console.error(error);
  }
};

const showErrorOefeningenOefesessie = function (err) {
  console.info('in de error van tonen oefensessies');
  console.error(err);
};
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********
const getOefensessies_leerling = function () {
  const url = `http://${lanIP}/projectOne/RietDeMeulemeester/home/oefensessies/`;
  token = localStorage.getItem('accessToken');
  console.info("in get oefensessies leerling");
  handleData(url, showOefensessies, showErrorOefensessies, 'GET', null, token);
};


const getOefensessie_info = function (oefensessieid) {
  const url = `http://${lanIP}/projectOne/RietDeMeulemeester/home/oefensessie/${oefensessieid}/`;
  token = localStorage.getItem('accessToken');
  console.info("in get oefensessie info");
  handleData(url, showOefensessieInfo, showErrorOefensessieInfo, 'GET', null, token);
};

const getInfoLeerling = function () {
  const url = `http://${lanIP}/projectOne/RietDeMeulemeester/home/`;
  token = localStorage.getItem('accessToken');
  console.info("in get info leerling");
  handleData(url, showInfoLeerling, showErrorInfoLeerling, 'GET', null, token);
};

const getAantallenLeerling = function () {
  const url = `http://${lanIP}/projectOne/RietDeMeulemeester/home/oefensessies/aantal/`;
  token = localStorage.getItem('accessToken');
  console.info("in get info aantal oefensessies leerling");
  handleData(url, showAantalOefensessiesLeerling, showErrorAantalOefensessiesLeerling, 'GET', null, token);
};

const getAantalOefeningenLeerling = function () {
  const url = `http://${lanIP}/projectOne/RietDeMeulemeester/home/oefeningen/aantal/`;
  token = localStorage.getItem('accessToken');
  console.info("in get info aantal oefeningen leerling");
  handleData(url, showAantalOefeningenLeerling, showErrorAantalOefeningenLeerling, 'GET', null, token);
};
// #endregion

// #region ***  Event Listeners - listenTo___            ***********
const listenToClickOefensessie = function (){
  for (const oefensessie of document.querySelectorAll('.js-oefensessie')) {
    oefensessie.addEventListener('click', function () {
      const oefensessieid =  this.getAttribute('data-oefensessieid');
      // console.info(`Oefeningen ${oefensessieid} ophalen`);
      token = localStorage.getItem('accessToken');      
      const url = `http://${lanIP}/projectOne/RietDeMeulemeester/home/oefeningen/${oefensessieid}/`
      handleData(url,showOefeningenOefesessie, showErrorOefeningenOefesessie, 'GET',  null ,token );
      getOefensessie_info(oefensessieid)
    });
  }
}

const listenToClickShutdown = function () {
  const shutdownknop = document.querySelector('.js-button-shutdown');
  shutdownknop.addEventListener('click', function () {
    console.log('Shutdown')
    socketio.emit('F2B_shutdown', null)
  });
};


const listenToUI = function () {
  //niet vergeten functie aan te roepen in de init !!!!!!!
};

const listenToSocket = function () {
  //niet vergeten functie aan te roepen in de init !!!!!!!
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });
  socketio.on('B2F_toon_info', function (msg) {
    const url = `http://${lanIP}/projectOne/RietDeMeulemeester/home/`;
    token = localStorage.getItem('accessToken');
    handleData(url, showOefensessies, showErrorOefensessies, 'GET', null, token);

  });
  
};

// #region ***  Init / DOMContentLoaded                  ***********
const init = function () {
  console.info('DOM geladen');
  token = localStorage.getItem('accessToken');
  
  
  htmlhome = document.querySelector('.js-welkom');
  htmlgebruiker = document.querySelector('.js-gebruiker');
  

  if (htmlhome){
    console.log('we zijn op de home pagina');
    getInfoLeerling();
    getOefensessies_leerling();
    getAantallenLeerling();
    getAantalOefeningenLeerling();  
  }
  listenToClickShutdown()
  listenToUI();
  listenToSocket();
};

document.addEventListener('DOMContentLoaded', init);
// #endregion





