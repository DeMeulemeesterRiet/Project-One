'use strict';

let token = '';
const lanIP = `${window.location.hostname}:5000`;
// const lanIP = `192.168.168.169:5000`;

const socketio = io(lanIP);

// #region ***  DOM references                           ***********
let htmlgrafiek,htmlinloggen,htmlhome;
let chart;
let html_wachtwoord, html_chatbox, html_button, html_naam;
let leerling_info
// #endregion

// #region ***  Authentication                           ***********
// #endregion Authentication

// #region ***  Callback-Visualisation - show___         ***********
const showInitGrafiek = function(){
  try {
    var options = {
      chart: {
        height: 280,
        type: "area",
        zoom: {
          autoScaleYaxis: true,
          zoomedArea: {
            fill: {
              color: '#A3D483',
              opacity: 0.4
            },
            stroke: {
              color: '#3F6526',
              opacity: 0.4,
              width: 1
            }
          }
        }
      },
      dataLabels: {
        enabled: false
      },
      tooltip: {
          x: {
            format: 'dd MMM yyyy HH:mm'
          }
        },
      series: [],
      stroke: {curve: 'smooth'},
      xaxis: {type: 'datetime'},
      noData: { text: 'Loading...' },
      colors:['#C6E6B0']
            
    };

  chart = new ApexCharts(document.querySelector(".js-chart"), options);

  chart.render();

  } catch (error) {
    console.error(error)
  }
}

const showChartRecords = function (jsonObject) {
  try {
    // console.info(jsonObject);
    console.info("zit in showChartRecords")
    // let htmlstring = '';
    // htmlstring += `
    //   <tr class="c-row js-header">
    //       <td class="c-cell"><strong>Date time</strong></td>
    //       <td class="c-cell"><strong>Amount</strong></td>
    //   </tr>`;
    // for (const record of jsonObject.records) {
    //   // console.info(record);
    //   htmlstring += `
    //     <tr class="c-row">	
    //       <td class="c-cell">${record.datumtijd}</div>
    //       <td class="c-cell">${record.waarde} °C</div>
    //     </tr>
    //     `;

    //   // const timestamp = new Date(`${record.datumtijd} GMT+0200`).getTime();
    //   // data += `{x: ${timestamp},y: ${record.waarde} }`
      

    // }
    // document.querySelector('.js-table').innerHTML = htmlstring;
    
    let data = [];

    jsonObject.records.forEach(record => {
      // const timestamp = new Date(`${record.datumtijd} GMT+0200`).getTime(); // Assuming each record has a dateString property
      const timestamp = new Date(`${record.datumtijd}`).getTime();
      data.push({ x: timestamp, y: record.waarde });
    });
    chart.updateSeries([{
      data: data
    }])
    chart.zoomX(((data.slice(-1)[0].x)-604800000), (data.slice(-1)[0].x))  // zoom instellen op laatste dag gemeten data tot 1 week ervoor
    
  } catch (error) {
    console.error(error)  
  }
  
//   // chart.render();
//   let htmlstring = '';
//   htmlstring += `test`
// //   htmlstring += `
//     <tr class="c-row js-header">
//         <td class="c-cell"><strong>Date</strong></td>
//         <td class="c-cell"><strong>Amount</strong></td>
//     </tr>`;
//   for (const record of jsonObject.status) {
//     // console.info(record);
//     htmlstring += `
//       <tr class="c-row">	
//         <td class="c-cell">${record.date}</div>
//         <td class="c-cell">${record.amount}ml</div>
//       </tr>
//       `;
//   }
  // document.querySelector('.js-chart').innerHTML = htmlstring;
};
const showErrorChartRecords = function (err) {
  console.info('in de error van tonen grafiek');
  console.error(err);
};
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********
const getRecordsData = function () {
  console.info('je geraakt in de getRecordsData')
  const url = `http://${lanIP}/projectOne/RietDeMeulemeester/historiek/`;
  console.log(url)
  handleData(url, showChartRecords, showErrorChartRecords);
};
// #endregion

// #region ***  Event Listeners - listenTo___            ***********
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
  
  socketio.on('B2F_new_logging', function (msg) {
    getRecordsData();
  });
  
  socketio.on('B2F_historiek_tonen', function (msg) {
    window.location.href = `historiek.html`;
    getRecordsData();
  });
};
// #endregion

// #region ***  Init / DOMContentLoaded                  ***********
const init = function () {
  console.info('DOM geladen');
  token = localStorage.getItem('accessToken');
  
  htmlgrafiek = document.querySelector('.js-table');

  if (htmlgrafiek) {
    console.info("dit is pagina historiek")
    showInitGrafiek()
    getRecordsData()
  }

  listenToUI();
  listenToSocket();
};

document.addEventListener('DOMContentLoaded', init);
// #endregion
