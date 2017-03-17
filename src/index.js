var fs = require('fs');
var moment = require('moment');

var express = require('express');
var app = express();
app.set('view engine', 'pug');
app.use(express.static('public'))

var MAPPINGS = {
  "machines": {
    "2F234454-CF6D-4A0F-ADF2-F4911BA9FFA6": "Zone A",
    "74278BDA-B644-4520-8F0C-720EAF059935": "Zone B"
  },
  "tools": {
    "136-4-14-210": "T1",
    "136-4-211-211": "T2",
  }
};

var LATEST_READINGS_FILE = './output.json';

function getReadings() {
  var readings = JSON.parse(fs.readFileSync(LATEST_READINGS_FILE, 'utf8'));

  var timestamp = moment.unix(readings["timestamp"]);

  var zoneUUID = readings["zoneUUID"];
  readings["zoneUUID"] = MAPPINGS["machines"][zoneUUID] || zoneUUID;

  var tagIDs = readings["tags"]
  var toolIDs = [];

  tagIDs.forEach(function(tagID) {
    toolIDs.push(MAPPINGS["tools"][tagID] || tagID);
  });

  toolIDs = toolIDs.filter(function(x) { return x.length != 0 }).sort();

  readings["tags"] = toolIDs;

  readings["toolCount"] = toolIDs.length;

  var since = timestamp.fromNow();

  readings["since"] = since;

  return readings;
}

app.get('/', function (req, res) {
  res.render('index', getReadings());
});

app.get('/latest_readings.json', function(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.send(JSON.stringify(getReadings()));
});

var port = process.env.PORT || 3000;
app.listen(port, "0.0.0.0");
