/**
* Map Rendering and Interface Javascript
* Feature properties: 
* "EASE_W6ID":10102,"name":"Tahtay Adiyabo","REGION_R2I":1,"W_NAME":"Tahtay Adiyabo","styleUrl":"#PolyStyle00","EASE_Wored":"Tahtay Adiyabo","W6ID":10102,
* "Area_km2":3911.757416,"styleHash":"-6104f216","LONG":37.793356,"FID":0,"EASE_ZoneN":"Western Tigray","LAT":14.42934,"EASE_Z4ID":101
*/
var infoWindow;
var geoJsonObjects;
var infowindow;
var map;
var variable;
var date;
var json = null;
var mapdata = null;

// Loading of the wareda map
$(document).ready(function(){
  // Build the google maps base
  var myLatlng = new google.maps.LatLng(9.195761, 40.498867);
  var mapOptions = {
    zoom: 7,
    center: myLatlng,
    mapTypeId: google.maps.MapTypeId.HYBRID,
    scaleControl: true,
    backgroundColor: 'transparent',
    panControl: false,
    streetViewControl: false,
    zoomControl: true,
    zoomControlOptions: {
      style: google.maps.ZoomControlStyle.DEFAULT,
      position: google.maps.ControlPosition.RIGHT_TOP
    } 
  };
  map = new google.maps.Map($('#map-canvas')[0], mapOptions);
  map.setTilt(0);

  // TopoJson rendering
  $.getJSON("../static/maps/ethiopia_waredas_full_topo.json", function(data){
        geoJsonObjects = topojson.feature(data, data.objects.ethiopia_waredas_full_converted_min)
        map.data.addGeoJson(geoJsonObjects); 
  }); 

  // Color each wareda
  map.data.setStyle(function(feature) {
    // Initialized to be all white
    return {
      fillColor: "#FFFFFF",
      strokeColor: "#FFFFFF",
      strokeWeight: 1
    };
  });
  // Set up the info window
  infowindow = new google.maps.InfoWindow({});
  // When a wareda is clicked, display pertinent information.
  map.data.addListener('click', function(event) {
    var name = event.feature.getProperty('name');
    var ease_w6id = parseInt(event.feature.getProperty('EASE_W6ID'));
    // Set window content
    infowindow.setContent(name);
    if (json != null && ease_w6id in json) {
      var val = json[ease_w6id].toString();
      val = name + ": " + val; 
      infowindow.setContent(val);
    }
    // Define where the info window should be located
    infowindow.setPosition(event.latLng);
    infowindow.open(map);
  });

  // When the user hovers, tempt them to click by outlining the letters.
  map.data.addListener('mouseover', function(event) {
    map.data.revertStyle();
    map.data.overrideStyle(event.feature, {
      fillOpacity: 1
    });
  });

  map.data.addListener('mouseout', function(event) {
    map.data.revertStyle();
  });

  // Only show map after fully loaded
  google.maps.event.addListenerOnce(map, 'tilesloaded', function(){
    // Loading of the map means the hiding of the loading canvas, which is on top of the map. 
    $("#loading-canvas").hide();
  });
});  


//Helper functions for RGB to HEX (Courtesy of StackOverflow)
function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}
