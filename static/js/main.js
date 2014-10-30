/**
* Map Rendering and Interface Javascript
*/
var infoWindow;
var geoJsonObjects;
var infowindow;

// Loading of the wareda map
$(document).ready(function(){
  // Build the google maps base
  var myLatlng = new google.maps.LatLng(9.195761, 40.498867);
  var mapOptions = {
    zoom: 6,
    center: myLatlng,
    mapTypeId: google.maps.MapTypeId.HYBRID,
    scaleControl: true,
    backgroundColor: 'transparent'
  };
  map = new google.maps.Map($('#map-canvas')[0], mapOptions);
  map.setTilt(0);

  // TopoJson rendering
  $.getJSON("../static/maps/ethiopia_waredas_full_topo.json", function(data){
        geoJsonObjects = topojson.feature(data, data.objects.ethiopia_waredas_full_converted_min)
        map.data.addGeoJson(geoJsonObjects); 
  }); 

  // Color each letter gray. Change the color when the isColorful property
  // is set to true.
  map.data.setStyle(function(feature) {
    // Determine the color needed
    var area = feature.getProperty('Area_km2');
    var color = area > 1000.0 ? 'blue' : 'red';
    return {
      fillColor: color,
      strokeColor: color,
      strokeWeight: 1
    };
  });
  // Set up the info window
  infowindow = new google.maps.InfoWindow({});
  // When a wareda is clicked, display pertinent information.
  map.data.addListener('click', function(event) {
    // event.feature.setProperty('isColorful', true);
    var name = event.feature.getProperty('name');
    infowindow.setContent(name);
    infowindow.setPosition(event.latLng);
    infowindow.open(map);
  });

  // When the user hovers, tempt them to click by outlining the letters.
  // Call revertStyle() to remove all overrides. This will use the style rules
  // defined in the function passed to setStyle()
  map.data.addListener('mouseover', function(event) {
    map.data.revertStyle();
    map.data.overrideStyle(event.feature, {
      fillOpacity: 1
      // strokeWeight: 8
    });
  });

  map.data.addListener('mouseout', function(event) {
    map.data.revertStyle();
  });
});

//Experimental KML rendering
// var waredaLayer = new google.maps.KmlLayer({
//   url: 'https://www.dropbox.com/s/ptq675yo6f2jrrp/ethiopia_waredas.kml'
// });
// waredaLayer.setMap(map);
