const request = require('request');
const https = require('https');
const fs = require('fs');
// const cheerio = require('cheerio');
const argAry = process.argv;
var allTrucks = null;
var args = {};

for (var i = 0; i < argAry.length; i++) {
    var arg = argAry[i];

    if (arg.indexOf('-') > -1) {
        var val = argAry[i + 1];

        args[arg.replace(/-/g, '')] = (num(val) ? parseInt(val) : val);
    }
}

function num(str) {
    return !isNaN(str);
}

function priceHandler(html) {
    var kellyLow = html.indexOf('PrivatePartyExcellentRangeLow'); // /\{[^\{]*PrivatePartyExcellentRangeLow[^\}]*\}/g

    console.log(kellyLow);
}

if (args.truck_csv) {
    allTrucks = args.truck_csv.split(',');
} else {
    allTrucks = fs.readFileSync('marketplace.csv', 'utf8').split(',');
}

for (var i = 0; i < allTrucks.length; i++) {
    request(allTrucks[i], function (error, response, body) {
        if (body) {
            priceHandler(body.toString());
        }
    });
}



