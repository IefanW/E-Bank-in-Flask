var map = new BMap.Map("allmap");
var point = new BMap.Point(116.331398,39.897445);
map.centerAndZoom(point,12);
map.enableScrollWheelZoom();
var geolocation = new BMap.Geolocation();
geolocation.getCurrentPosition(function(r){
if(this.getStatus() == BMAP_STATUS_SUCCESS){
		var mk = new BMap.Marker(r.point);
		map.panTo(r.point);
		alert('Your location：'+r.point.lng+','+r.point.lat);
		var local = new BMap.LocalSearch(map, {
  			renderOptions:{map: map}
 		});
		var pStart = new BMap.Point(r.point.lng,r.point.lat);
 		var pEnd = new BMap.Point(r.point.lng+0.07,r.point.lat+0.07);
 		var bs = new BMap.Bounds(pStart,pEnd);
 		local.searchInBounds("银行", bs);
 		var polygon = new BMap.Polygon([
  			new BMap.Point(pStart.lng,pStart.lat),
  			new BMap.Point(pEnd.lng,pStart.lat),
			new BMap.Point(pEnd.lng,pEnd.lat),
		  	new BMap.Point(pStart.lng,pEnd.lat)
		  	], {strokeColor:"blue", strokeWeight:6, strokeOpacity:0.5});
 		map.addOverlay(polygon);
}
else {
		alert('failed'+this.getStatus());
}
},{enableHighAccuracy: true});