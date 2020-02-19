var express = require('express');
var app = express();
const bodyParser = require('body-parser');

var path = require('path');

app.use(express.static('public'))

const pool = require('./pool-factory');
const connectionMiddleware = require('./connection-middleware');

app.use(connectionMiddleware(pool));

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());


const PORT = process.env.PORT || 3000


app.get('/', function (req, res) {
    res.sendFile(path.join(__dirname + '/public/index.html'));
});
app.get('/analytics', function (req, res) {
    res.sendFile(path.join(__dirname + '/public/analytics.html'));
});
app.get('/planos', function (req, res) {
    res.sendFile(path.join(__dirname + '/public/planos.html'));
});
app.get('/insight', function (req, res) {
    res.sendFile(path.join(__dirname + '/public/insight.html'));
});


app.post('/user', (req, res) => {

    var datetime = new Date().toISOString().slice(0, 19).replace('T', ' ');
    let sql = `INSERT INTO customers(insertDate, name,address,phone,linkedin,email)  
            VALUES(?,?,?,?,?,?)`;
    var values = [datetime, req.body.name, req.body.address, req.body.phone, req.body.linkedin, req.body.email]
    req.connection.query(sql, values, (err, result) => {
        if(err) return next(err);
        res.json(result);
    })

})


app.get('/user', (req, res) => {
    let sql = `SELECT * from customers`;
    req.connection.query(sql, (err, products) => {
        if(err) return next(err);
        res.json(products);
    })
})

app.listen(PORT, () => console.log(`Listening on ${PORT}`));

