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
    "136-4-239-109": "T-001",
    "136-4-103-109": "T-002",
    "136-4-81-109": "T-003",
    "136-4-79-109": "T-004",
    "136-4-94-109": "T-005",
    "136-4-147-109": "T-006",
    "136-4-117-10": "T-007",
    "136-4-58-108": "T-008",
    "136-4-101-0": "T-009",
    "136-4-77-10": "T-010",
    "136-4-103-108": "T-011"
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
