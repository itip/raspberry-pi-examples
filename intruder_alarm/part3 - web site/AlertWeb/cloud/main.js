require('cloud/app.js');

/* After adding an alert we'll send an email */
var mandrillKey = '<MANDRILL_KEY>';

var emailSender = '<EMAIL_SENDER>'
var emailRecipient = '<EMAIL_RECIPIENT>'

var Mandrill = require('mandrill');
Mandrill.initialize(mandrillKey);

Parse.Cloud.afterSave("Alert", function(request) {

  if (mandrillKey == '') {
    // Can't send email as key not yet set.
    response.success("This will send an email once the key has been set.");
    return;
  }

  Mandrill.sendEmail({
    message: {
      text: "Alert received at " + request.object.createdAt + " " +
        request.object.get('picture').url(),
      subject: "An alert was received",
      from_email: emailSender,
      to: [{
        email: emailRecipient
      }]
    },
    async: true
  }, {
    success: function(httpResponse) {
      console.log(httpResponse);
      response.success("Email sent!");
    },
    error: function(httpResponse) {
      console.error(httpResponse);
      response.error("Uh oh, something went wrong");
    }
  });
});
