/**
* Maps Javascript
*/
var infoWindow;

function infoWindowContent(name, description) {
   content =   '<div class="FT_infowindow"><h3>' + name + 
               '</h3><div>' + description + '</div></div>';
   return content;
}

//Initialization
var myLatlng = new google.maps.LatLng(9.195761, 40.498867);
var mapOptions = {
  zoom: 6,
  center: myLatlng,
  mapTypeId: google.maps.MapTypeId.HYBRID,
  scaleControl: true

};
var map = new google.maps.Map(document.getElementById("map-canvas"),
    mapOptions);
map.setTilt(0);

//Country overlay
var layer = new google.maps.FusionTablesLayer({
  query: {
    select: 'kml_4326', 
    from: '420419', 
    where: "'name_0' = 'Ethiopia'"
  },
  map: map,
  suppressInfoWindows: true
});

infoWindow = new google.maps.InfoWindow();
google.maps.event.addListener(layer, "click", function(event) {
  infoWindow.close();
  infoWindow.setContent(infoWindowContent(event.row.name_1.value,event.row.name_0.value));
  infoWindow.setPosition(event.latLng);
  infoWindow.open(map);
});
