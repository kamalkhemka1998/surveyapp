# cross-origin


[![npm version](https://badge.fury.io/js/cross-origin.svg)](http://badge.fury.io/js/cross-origin)


> cross-origin for express

## Installation

    npm install cross-origin --save


## Usage

    var express = require('express');
    var app = express();
    var crossOrigin = require('cross-origin');
    app.use(crossOrigin);
    ...


* origin: *
* allowMethods: GET,HEAD,PUT,POST,DELETE,PATCH
