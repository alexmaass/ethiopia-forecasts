/**
* Maps Javascript
*/
L.mapbox.accessToken = 'pk.eyJ1IjoiYW04MzgiLCJhIjoiMmdjdlpKUSJ9.DIBX2rAhuqs3WvQ-rrbHCg';
var mapboxTiles = L.tileLayer('https://{s}.tiles.mapbox.com/v4/examples.map-i87786ca/{z}/{x}/{y}.png', {
  attribution: '<a href="http://www.mapbox.com/about/maps/" target="_blank">Terms &amp; Feedback</a>'
});

var lat = 39.647469;
var lng = -101.250000;
var map = L.map('map').addLayer(mapboxTiles).setView([lat, lng], 4);