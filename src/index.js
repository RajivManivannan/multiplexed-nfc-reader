var fs = require('fs');
var moment = require('moment');

var express = require('express');
var app = express();
app.set('view engine', 'pug');
app.use(express.static('public'))

var MAPPINGS = {
  "machines": {
    "2F234454-CF6D-4A0F-ADF2-F4911BA9FFA6": "Machine A Zone",
    "74278BDA-B644-4520-8F0C-720EAF059935": "Machine B Zone"
  },
  "tools": {
    "136-4-206-0": "T-01",
    "136-4-60-108": "T-02",
    "136-4-78-109": "T-03",
    "136-4-24-109": "T-04",
    "136-4-136-0": "T-05",
    "136-4-144-171": "T-06",
    "136-4-117-10": "T-07",
    "136-4-58-108": "T-08",
    "136-4-101-0": "T-09",
    "136-4-77-10": "T-10"
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

  readings["tags"] = toolIDs.sort();

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
