import com.atlassian.jira.bc.projectroles.ProjectRoleService
import com.atlassian.jira.component.ComponentAccessor
import com.atlassian.jira.mail.Email
import com.atlassian.jira.project.Project
import com.atlassian.jira.project.ProjectManager
import com.atlassian.jira.security.roles.ProjectRole
import com.atlassian.jira.security.roles.ProjectRoleActors
import com.atlassian.jira.security.roles.ProjectRoleManager
import com.atlassian.jira.util.ErrorCollection
import com.atlassian.jira.util.SimpleErrorCollection
import com.atlassian.jira.user.ApplicationUser
import org.apache.log4j.Category
import org.apache.log4j.Logger
import com.atlassian.jira.mail.Email
import com.atlassian.mail.server.SMTPMailServer
Category log = Category.getInstance("com.onresolve.jira.groovy")
log.setLevel(org.apache.log4j.Level.DEBUG)


//Declaration des variables
def baseUrl = ComponentAccessor.getApplicationProperties().getString("jira.baseurl")
Set<ApplicationUser> Users
ProjectRoleService projectRoleService = (ProjectRoleService) ComponentAccessor.getComponentOfType(ProjectRoleService.class);
ProjectRoleManager projectRoleManager = (ProjectRoleManager) ComponentAccessor.getComponentOfType(ProjectRoleManager.class);
ProjectManager projectManager = ComponentAccessor.getProjectManager();

def groupManager = ComponentAccessor.getGroupManager()



//Project project = projectManager.getProjectObjByKey('SUP')
//ProjectRole administrator = projectRoleManager.getProjectRole("Key Users");


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

Users = groupManager.getUsersInGroup("test-leo")
// Do your thing
for(ApplicationUser user:Users){
	if(user.isActive()){
		def token =ComponentAccessor.getUserUtil().generatePasswordResetToken(user)
		String Url = baseUrl+"/secure/ResetPassword!default.jspa?os_username="+user.username+"&token="+token.getToken()
		String mailBody = "Bonjour,<br>" +
				" <br>" +
				"Vos acc&egrave;s &agrave; JIRA ont &eacute;t&eacute; initialis&eacute;s. En cliquant sur le lien suivant, vous pourrez renseigner un mot de passe pour y acc&eacute;der avec votre compte personnalis&eacute; :<br>" +
				"Votre login JIRA : " + user.username +"<br>"+
				"<a href=" + Url + ">"+Url+"</a><br>" +
				" <br>" +
				"Le lien reste actif durant 24H. En cas de probl&egrave;me, ou de d&eacute;passement du d&eacute;lai, merci d&#39;aller sur le serveur JIRA pour faire une demande de mot de passe<br>" +
				" <br>" +
				" <br>" +
				"Cordialement,<br>" +
				" <br>" +
				"L&#39;&eacute;quipe Support"


		sendEmail(user.emailAddress, "Reinitialisation du Mot de passe JIRA",mailBody)

	}
}


