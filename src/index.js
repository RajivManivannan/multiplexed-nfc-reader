var fs = require('fs');
var moment = require('moment');

var express = require('express');
var app = express();
app.set('view engine', 'pug');
app.use(express.static('public'))

var LATEST_READINGS_FILE = './output.json';

function getReadings() {
  var readings = JSON.parse(fs.readFileSync(LATEST_READINGS_FILE, 'utf8'));

  var timestamp = moment.unix(readings["timestamp"]);

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