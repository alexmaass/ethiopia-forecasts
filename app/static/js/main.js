/**
* Maps Javascript
*/

//Initialization
var myLatlng = new google.maps.LatLng(9.195761, 40.498867);
var mapOptions = {
  zoom: 6,
  center: myLatlng,
  // mapTypeId: google.maps.MapTypeId.SATELLITE
  mapTypeId: google.maps.MapTypeId.HYBRID

};
var map = new google.maps.Map(document.getElementById("map-canvas"),
    mapOptions);
map.setTilt(0);

//Country overlay
var world_geometry = new google.maps.FusionTablesLayer({
  query: {
    select: 'kml_4326', 
    from: '420419', 
    where: "'name_0' = 'Ethiopia'"
  },
  map: map,
  suppressInfoWindows: false
});

