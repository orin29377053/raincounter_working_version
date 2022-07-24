(function (window) {
    "use strict";

    // baselayers
    let baselayers, all_layers
    let layer60min, layer10min, layer3hr, layer6hr, layer12hr, layer24hr, layertoday, layer48hr, layer72hr
    // overlayers
    let overlayers, cwbPoint, eqPoint
    let controls_windows, controls_zoom
    let rainLegend;
    // create a map
    let mapOptions = {
        preferCanvas: true,
        zoomControl: false,
        attributionControl: true,
        maxZoom: 16,
        minZoom: 4
    };
    let idw_data

    let attribution = `&copy; <a target="_blank" rel="noopener noreferrer" href="http://www.openstreetmap.org/copyright">OSM</a>`;

    let map = L.map("heatmap", mapOptions).setView([23.77, 120.88], 8);
    let rainGradient = {
        0: "#F1F1F1",
        1: "#D3EFFF",
        3: "#63BBDA",
        6: "#3CA1CE",
        8: "#1989B3",
        10: "#2253D8",
        15: "#18A218",
        20: "#88E23F",
        25: "#CAE085",
        30: "#FAFF08",
        35: "#FFD008",
        40: "#F5AE04",
        50: "#FF8700",
        60: "#FF6F00",
        70: "#F95230",
        80: "#CE391B",
        90: "#FF4C50",
        110: "#D81E22",
        130: "#9A1113",
        150: "#AF1E82",
        200: "#E060BA",
        300: "#FBB9FB",
    };
    let mobile_rainGradient = {
        0: "#F1F1F1",
        3: "#63BBDA",
        6: "#3CA1CE",
        10: "#2253D8",
        15: "#18A218",
        25: "#CAE085",
        35: "#FFD008",
        50: "#FF8700",
        70: "#F95230",
        90: "#FF4C50",
        130: "#9A1113",
        150: "#AF1E82",
        200: "#E060BA",
        300: "#FBB9FB",
    };
    
    let rainIDWOptions = {
        opacity: 0.5,
        maxZoom: mapOptions.maxZoom,
        minZoom: mapOptions.minZoom,
        cellSize: 3,
        exp: 2,
        gradient: rainGradient,
        dataType: 2,
        cwb_station_range: 10,
        minVal: 0.0,
        maxVal: 300.0
    };


    map.on("overlayadd baselayerchange", event => {
        document
            .getElementsByClassName("leaflet-idwmap-layer leaflet-layer leaflet-zoom-animated")[0]
            .style.zIndex = "0";
    });



    // disable overlayers checkbox when zoomend and the baselayer is temperature idw
    map.on("zoomend", function (event) {
        for (let key in baselayers) {
            if (key.includes("Temperature") && map.hasLayer(baselayers[key])) {
                let layers = document.getElementsByClassName("leaflet-control-layers-selector");
                for (let i = layers.length - 1; i >= 0; i--) {
                    if (layers[i].type === "checkbox" && layers[i].nextSibling.innerText.includes("Contour")) {
                        layers[i].disabled = true;
                    }
                }
            }
        }
    })

    let Stamen_Terrain = new L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.{ext}', {
        attribution: attribution,
        minZoom: mapOptions.minZoom,
        maxZoom: mapOptions.maxZoom,
        ext: 'png',
        opacity: 0.8
    }).addTo(map);

    var greenIcon = new L.Icon({
        iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });
    
    var redIcon = new L.Icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });
    var orangeIcon = new L.Icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });
    var violetIcon = new L.Icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-violet.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    const station_data_popup = (value) => {
        return (
            `<h6>${value.stationId} ${value.locationName}</h6>
              <p class="my-2">更新時間：${value.time.obsTime}</p>
              <ul class="pl-3">
                <li>${value.parameter[4].parameterValue}</li>
                <li>
                  經緯度：[ ${value.lat}, ${value.lon} ]
                </li>
                <li>高度：${value.weatherElement[0].elementValue} m</li>
                <li>
                  10分鐘累積雨量：
                  ${value.weatherElement[2].elementValue == -998.0 ? "0.00"
                : value.weatherElement[2].elementValue}
                  mm
                </li>
                <li>
                  60分鐘累積雨量：
                  ${value.weatherElement[1].elementValue == -998.0 ? "0.00"
                : value.weatherElement[1].elementValue}
                  mm
                </li>
                <li>
                  3小時累積雨量：
                  ${value.weatherElement[3].elementValue == -998.0 ? "0.00"
                : value.weatherElement[3].elementValue}
                  mm
                </li>
                <li>
                  6小時累積雨量：
                  ${value.weatherElement[4].elementValue == -998.0 ? "0.00"
                : value.weatherElement[4].elementValue}
                  mm
                </li>
                <li>12小時累積雨量：${value.weatherElement[5].elementValue} mm</li>
                <li>24小時累積雨量：${value.weatherElement[6].elementValue} mm</li>
                <li>本日累積雨量：${value.weatherElement[7].elementValue} mm</li>
                <li>48小時累積雨量：${value.weatherElement[8].elementValue} mm</li>
                <li>72小時累積雨量：${value.weatherElement[9].elementValue} mm</li>
              </ul>`
        )
    }
    function crtTimeFtt(value, row) {
        if (value != null) {
            let date = new Date(value);
            date.setHours(date.getHours() + 8);
            return date.getFullYear() + '-' + add0(date.getMonth() + 1) + '-' + add0(date.getDate()) + ' ' + add0(date.getHours()) + ':' + add0(date.getMinutes()) + ':' + add0(date.getSeconds());
        }
    }
    function add0(Completion) {
        return Completion < 10 ? "0" + Completion : Completion;
    }
    const raincounter_data_popup = (value) => {
        let sta = ""
        switch (value.status) {
            case "working":
                sta = "運作中"
                break;
            case "error":
                sta = "設備異常"
                break;
            case "low_power":
                sta = "低電量"
                break;
            case "unregister":
                sta = "未註冊"
                break;
            case "deactivate":
                sta = "停用"
                break;
            default:
                sta = "-"
                break;
        }
        return (
            `<h6>${value.device} / ${value.name}</h6>
              <p class="my-2">更新時間：${crtTimeFtt(value.last_update)}</p>
              <ul class="pl-3">
                <li style="font-weight:bold;">${sta}</li>
                <li>經緯度：[ ${value.y.toFixed(3)}, ${value.x.toFixed(3)} ]</li>
                <li>10分鐘累積雨量：${value["10min"] == -333 ? "儀器故障" : value["10min"]} mm</li>
                <li>60分鐘累積雨量：${value["60min"] == -333 ? "儀器故障" : value["60min"]} mm</li>
                <li>3小時累積雨量：${value["3h"] == -333 ? "儀器故障" : value["3h"]} mm</li>
                <li>6小時累積雨量：${value["6h"] == -333 ? "儀器故障" : value["6h"]} mm</li>
                <li>12小時累積雨量：${value["12h"] == -333 ? "儀器故障" : value["12h"]} mm</li>
                <li>24小時累積雨量：${value["24h"] == -333 ? "儀器故障" : value["24h"]} mm</li>
                <li>本日累積雨量：${value["today"] == -333 ? "儀器故障" : value["today"]} mm</li>
                <li>48小時累積雨量：${value["48h"] == -333 ? "儀器故障" : value["48h"]} mm</li>
                <li>72小時累積雨量： ${value["72h"] == -333 ? "儀器故障" : value["72h"]}mm</li>
              </ul>`
        )
    }

    let rrr_data = {}

    const layerAdd = (urls, first = false, ourdata) => {
        Promise.all(urls.map(url => makeRequest('GET', url)))
            .then(texts => {
                // parse all texts to json objects
                return texts.map(txt => JSON.parse(txt));
            })
            .then(jsons => {
                if (!first) {
                    all_layers.eachLayer((layer) => map.removeLayer(layer)).clearLayers();
                    map.removeLayer(cwbPoint)
                    map.removeLayer(eqPoint)
                    map.removeControl(controls_windows)
                } else {
                    if ($(document).width() < 600) {
                        rainLegend = new L.control.IDWLegend(mobile_rainGradient, {
                            position: 'bottomright',
                            unit: "單位: 毫米 (mm)"
                        }).addTo(map);
                        controls_zoom = L.control.zoom({ position: "bottomleft" }).addTo(map)
                        
                    } else {
                        rainLegend = new L.control.IDWLegend(rainGradient, {
                            position: 'bottomright',
                            unit: "單位: 毫米 (mm)"
                        }).addTo(map);
                        controls_zoom = L.control.zoom({ position: "bottomleft" }).addTo(map)
                    
                    }
                    
                }
                
                let cwb_rain = {
                    "60min": [],
                    "10min": [],
                    "3hr": [],
                    "6hr": [],
                    "12hr": [],
                    "24hr": [],
                    "today": [],
                    "48hr": [],
                    "72hr": [],
                }
                let interval = Object.keys(cwb_rain)

             


                
                cwbPoint = L.markerClusterGroup();
                eqPoint = new L.layerGroup();
                
                $(jsons[0].records.location).each((ind, val) => {
                    ind == 0 && $("#data_time").empty().append(val.time.obsTime)
                    let lat = parseFloat(val.lat),
                        lon = parseFloat(val.lon)
                    $(val.weatherElement).each((ind0, val0) => {
                        let dd = parseFloat(val0.elementValue)
                        dd < 0 ? dd = 0 : dd = dd;
                        ind0 != 0 && cwb_rain[interval[ind0 - 1]].push([lat, lon, dd])
                    })
                    cwbPoint.addLayer(L.marker(new L.LatLng(lat, lon)).bindPopup(station_data_popup(val)))
                })
                if (first) {
                    rrr_data = cwb_rain["72hr"]
                }
                
                   
                $(ourdata).each((ind, ele) => {                    
                    if (ele.y && ele.x) {
                        if (ele.status == "deactivate") {
                            eqPoint.addLayer(L.marker([ele.y, ele.x], { icon: redIcon }).bindPopup(raincounter_data_popup(ele)))
                        } else if (ele.status == "low_power") {
                            eqPoint.addLayer(L.marker([ele.y, ele.x], { icon: orangeIcon }).bindPopup(raincounter_data_popup(ele)))
                        } else if (ele.status == "error") {
                            eqPoint.addLayer(L.marker([ele.y, ele.x], { icon: violetIcon }).bindPopup(raincounter_data_popup(ele)))
                        }else {                            
                            eqPoint.addLayer(L.marker([ele.y, ele.x], { icon: greenIcon }).bindPopup(raincounter_data_popup(ele)))
                        }
                        
                        
                    }
                })
                

                layer60min = new L.idwLayer(cwb_rain["60min"], rainIDWOptions);
                layer10min = new L.idwLayer(cwb_rain["10min"], rainIDWOptions);
                layer3hr = new L.idwLayer(cwb_rain["3hr"], rainIDWOptions);
                layer6hr = new L.idwLayer(cwb_rain["6hr"], rainIDWOptions);
                layer12hr = new L.idwLayer(cwb_rain["12hr"], rainIDWOptions);
                layer24hr = new L.idwLayer(cwb_rain["24hr"], rainIDWOptions);
                layertoday = new L.idwLayer(cwb_rain["today"], rainIDWOptions);
                layer48hr = new L.idwLayer(cwb_rain["48hr"], rainIDWOptions);
                layer72hr = new L.idwLayer(cwb_rain["72hr"], rainIDWOptions);
            
                all_layers = L.layerGroup([
                    layer60min,
                    layer10min,
                    layer3hr,
                    layer6hr,
                    layer12hr,
                    layer24hr,
                    layertoday,
                    layer48hr,
                    layer72hr
                ])

                baselayers = {
                    "10分鐘累積雨量": layer10min,
                    "60分鐘累積雨量": layer60min.addTo(map),
                    "3小時累積雨量": layer3hr,
                    "6小時累積雨量": layer6hr,
                    "12小時累積雨量": layer12hr,
                    "24小時累積雨量": layer24hr,
                    "本日累積雨量": layertoday,
                    "48小時累積雨量": layer48hr,
                    "72小時累積雨量": layer72hr,
                };

                overlayers = {
                    // contour layers
                    // "PM2.5 Contour Interval: 10": contourInterval10,
                    "中央氣象局": cwbPoint,
                    "ULTRON 雨量計": eqPoint,
                };
                if ($(document).width() < 600) {
                    controls_windows = L.control.layers(baselayers, overlayers, {
                        position: "topleft",
                        collapsed: true,
                        autoZIndex: true,
                    }).addTo(map);
                } else {
                    controls_windows = L.control.layers(baselayers, overlayers, {
                        position: "topleft",
                        collapsed: false,
                        autoZIndex: true,
                    }).addTo(map);
                }

                
                
                // idw_data = L.oupdata()
                // console.log(L.oupdata())
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    let cwb_url = ["https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0002-001/?Authorization=CWB-545F04AD-2B89-449A-B5D1-DB91A30D87D2&"]
        
    $(document).on('click', "#update_data", () => {
        let url = ["https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0002-001/?Authorization=CWB-545F04AD-2B89-449A-B5D1-DB91A30D87D2&"]
        // layerAdd(url)
        $.ajax({
            type: "GET",
            url: "api/get_raincounter_eq/",
            // data: "data",
            dataType: "json",
            success: function (response) {
                layerAdd(cwb_url, false, response)
                // layerAdd(["./static/data/0318_data_all.json"], true,response)
            }
        });

    })

    L.simpleMapScreenshoter({
        domtoimageOptions: { crossOrigin: 'anonymous',cacheBust: true, }, 
        cropImageByInnerWH: true,
        hidden: false,
        // preventDownload: true,
        screenName: 'Rain_heatmap_'+new Date().toLocaleDateString("zh",{year: "numeric",month: "2-digit",day: "2-digit"}).replaceAll("/","")+"_"+new Date().toLocaleTimeString().replaceAll(":","-").slice(2,7),
        hideElementsWithSelectors: ['.leaflet-control-container'],
        mimeType: 'image/png',
        caption: null
    }).addTo(map)
    // L.easyPrint({
    //     title: 'My awesome print button',
    //     position: 'bottomright',
    //     sizeModes: ['A4Portrait', 'A4Landscape']
    // }).addTo(map);

    $(document).ready(() => {
        $.ajax({
            type: "GET",
            url: "api/get_raincounter_eq/",
            dataType: "json",
            success: function (response) {
                layerAdd([cwb_url], true, response)
            }
        });
    })

    
    // make request function in promise
    // for loading json and geojson
    function makeRequest(method, url) {
        return new Promise(function (resolve, reject) {
            let xhr = new XMLHttpRequest();
            xhr.open(method, url);
            xhr.onload = function () {
                if (this.status >= 200 && this.status < 300) {
                    resolve(xhr.response);
                } else {
                    // If it fails, reject the promise with a error message
                    reject({
                        url: url,
                        status: this.status,
                        statusText: xhr.statusText
                    });
                }
            };
            xhr.onerror = function () {
                // Also deal with the case when the entire request fails to begin with
                // This is probably a network error, so reject the promise with an appropriate message
                reject({
                    url: url,
                    status: this.status,
                    statusText: xhr.statusText
                });
            };
            xhr.send();
        });
    }
    // make map a global variable
    window.map = map;
})(this);