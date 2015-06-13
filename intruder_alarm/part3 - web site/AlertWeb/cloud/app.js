/*
 - Restrict access (htaccess)
 - Add cloud function which uses afterSave(https://parse.com/docs/js/guide#cloud-code-aftersave-triggers)
 - Send email (register with Mandrill)

*/

// These two lines are required to initialize Express in Cloud Code.
express = require('express');
app = express();

// Global app configuration section
app.use(require('parse-express-https-redirect')()); // Redirect all calls to HTTPS
app.set('views', 'cloud/views'); // Specify the folder to find templates
app.set('view engine', 'ejs'); // Set the template engine
app.use(express.bodyParser()); // Middleware for reading request body


var helpUsername = 'admin';
var helpPassword = '<ADMIN_PASSWORD>'


app.get('/', express.basicAuth(helpUsername, helpPassword), function(req,
  res) {

  var Alert = Parse.Object.extend("Alert");
  var query = new Parse.Query(Alert);
  query.limit(20);
  query.descending("createdAt");

  query.find({
    success: function(results) {
      res.render('alerts', {
        alerts: results
      });
    },
    error: function(error) {
      res.render('alerts', {
        alerts: null
      });
    }
  });


});

// // Example reading from the request query string of an HTTP get request.
// app.get('/test', function(req, res) {
//   // GET http://example.parseapp.com/test?message=hello
//   res.send(req.query.message);
// });

// // Example reading from the request body of an HTTP post request.
// app.post('/test', function(req, res) {
//   // POST http://example.parseapp.com/test (with request body "message=hello")
//   res.send(req.body.message);
// });

// Attach the Express app to Cloud Code.
app.listen();
