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
var datatype = "RAIN";
var date = "1981-01-01";
var json = null;
var mapdata = null;

// Loading of the wareda map
$(document).ready(function(){
  // $('.dropdown-toggle').dropdown();
  
  // // Build the google maps base
  // var myLatlng = new google.maps.LatLng(9.195761, 40.498867);
  // var mapOptions = {
  //   zoom: 7,
  //   center: myLatlng,
  //   mapTypeId: google.maps.MapTypeId.HYBRID,
  //   scaleControl: true,
  //   backgroundColor: 'transparent'
  // };
  // map = new google.maps.Map($('#map-canvas')[0], mapOptions);
  // map.setTilt(0);

  // // TopoJson rendering
  // $.getJSON("../static/maps/ethiopia_waredas_full_topo.json", function(data){
  //       geoJsonObjects = topojson.feature(data, data.objects.ethiopia_waredas_full_converted_min)
  //       map.data.addGeoJson(geoJsonObjects); 
  // }); 

  // // Color each letter gray. Change the color when the isColorful property
  // // is set to true.
  // map.data.setStyle(function(feature) {
  //   // Determine the color needed
  //   var area = feature.getProperty('Area_km2');
  //   var color = area > 1000.0 ? 'blue' : 'red';
  //   return {
  //     fillColor: color,
  //     strokeColor: color,
  //     strokeWeight: 1
  //   };
  // });
  // // Set up the info window
  // infowindow = new google.maps.InfoWindow({});
  // // When a wareda is clicked, display pertinent information.
  // map.data.addListener('click', function(event) {
  //   // event.feature.setProperty('isColorful', true);
  //   var name = event.feature.getProperty('name');
  //   var ease_w6id = parseInt(event.feature.getProperty('EASE_W6ID'));
  //   // Set window content
  //   infowindow.setContent(name);
  //   if (json != null && ease_w6id in json) {
  //     var val = json[ease_w6id];
  //     console.log(val);
  //     infowindow.setContent(val.toString());
  //   }
  //   infowindow.setPosition(event.latLng);
  //   infowindow.open(map);
  // });

  // // When the user hovers, tempt them to click by outlining the letters.
  // // Call revertStyle() to remove all overrides. This will use the style rules
  // // defined in the function passed to setStyle()
  // map.data.addListener('mouseover', function(event) {
  //   map.data.revertStyle();
  //   map.data.overrideStyle(event.feature, {
  //     fillOpacity: 1
  //     // strokeWeight: 8
  //   });
  // });

  // map.data.addListener('mouseout', function(event) {
  //   map.data.revertStyle();
  // });

  // // Load map div
  // $("#map-canvas").show();

  // Menu sliding
  $("#accordian h3").click(function(){
      //slide up all the link lists
      $("#accordian ul ul").slideUp();
      //slide down the link list below the h3 clicked - only if its closed
      if(!$(this).next().is(":visible"))
      {
          $(this).next().slideDown();
      }
  })
});  

// $( "#testing-brand" ).click(function() {
//   // alert( "Handler for .click() called." );
//   // Make an ajax call to get back relevant content
//   $.ajax({
//     url: "/lookup",
//     type: "POST",
//     data: {
//       datatype: datatype,
//       date: date
//     },
//     success: function(result){
//       json = JSON && JSON.parse(result) || $.parseJSON(result);
//     }
//   });
// });

//Experimental KML rendering
// var waredaLayer = new google.maps.KmlLayer({
//   url: 'https://www.dropbox.com/s/ptq675yo6f2jrrp/ethiopia_waredas.kml'
// });
// waredaLayer.setMap(map);
