import com.atlassian.jira.component.ComponentAccessor
import org.apache.log4j.Category
import com.atlassian.jira.mail.Email
import com.atlassian.mail.server.SMTPMailServer

Category log = Category.getInstance("com.onresolve.jira.groovy")
log.setLevel(org.apache.log4j.Level.DEBUG)

//Declaration des variables
def user = ComponentAccessor.getUserManager().getUserByName("leo.kervizic")
def baseUrl = ComponentAccessor.getApplicationProperties().getString("jira.baseurl")

// Fonction Mail
def sendEmail(String emailAddr, String subject, String body) {
    SMTPMailServer mailServer = ComponentAccessor.getMailServerManager().getDefaultSMTPMailServer()
    if (mailServer) {
        Email email = new Email(emailAddr)
        email.setMimeType("text/html");
        email.setSubject(subject)
        email.setBody(body)
        mailServer.send(email)
        log.debug("Mail sent")
    } else {
        log.warn("Please make sure that a valid mailServer is configured")
    }
}

def token = ComponentAccessor.getUserUtil().generatePasswordResetToken(user)
String Url = baseUrl + "/secure/ResetPassword!default.jspa?os_username=" + user.username + "&token=" + token.getToken()
String mailBody = "Bonjour,<br/>" +
		" <br/>" +
		"Vos acc&egrave;s &agrave; JIRA ont &eacute;t&eacute; initialis&eacute;s. En cliquant sur le lien suivant, vous pourrez renseigner un mot de passe pour y acc&eacute;der avec votre compte personnalis&eacute; :<br>" +
		"Votre login JIRA : " + user.username +"<br/><br/>"+
		"<a href=" + Url + ">Changer votre mot de passe</a><br/>" +
		" <br/><br/>" +
		"Le lien reste actif durant 24H. En cas de probl&egrave;me, ou de d&eacute;passement du d&eacute;lai, merci de vous connecter sur votre serveur JIRA pour demander un nouveau mot de passe.<br>" +
		" <br/>" +
		" <br/>" +
		"Cordialement,<br/>" +
		" <br/>" +
		"L&#39;&eacute;quipe Admin"

sendEmail(user.emailAddress, "Reinitialisation du Mot de passe JIRA", mailBody)
