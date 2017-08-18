import com.atlassian.crowd.embedded.api.CrowdService
import com.atlassian.crowd.embedded.api.User
import com.atlassian.crowd.embedded.api.UserWithAttributes
import com.atlassian.crowd.embedded.impl.ImmutableUser
import com.atlassian.jira.bc.JiraServiceContextImpl
import com.atlassian.jira.bc.user.search.UserSearchParams
import com.atlassian.jira.bc.user.search.UserSearchService
import com.atlassian.jira.bc.user.UserService
import com.atlassian.jira.component.ComponentAccessor
import com.atlassian.jira.user.ApplicationUser
import com.atlassian.jira.user.ApplicationUsers
import com.atlassian.jira.user.util.UserManager
import com.atlassian.jira.user.util.UserUtil
import com.atlassian.jira.user.util.UserUtilImpl
import java.io.File
import java.io.Reader
import org.apache.log4j.Category
 
Category log = log;
log.setLevel(org.apache.log4j.Level.DEBUG);

//To manage users data
UserManager userManager = ComponentAccessor.getUserManager()
UserSearchService userSearchService = ComponentAccessor.getComponent(UserSearchService.class)
UserService userService = ComponentAccessor.getComponent(UserService.class)
UserUtil userUtil = ComponentAccessor.getUserUtil()
CrowdService crowdService = ComponentAccessor.getCrowdService()

//To create new users
UserService.CreateUserValidationResult createUserValidationResult
//To update existing users
ApplicationUser updateUser
UserService.UpdateUserValidationResult updateUserValidationResult

ApplicationUser loggedUser = ComponentAccessor.jiraAuthenticationContext?.getLoggedInUser()
final CreateUserRequest UserRequest = CreateUserRequest.withUserDetails(loggedUser, "","", "", "")
def serviceContext = new JiraServiceContextImpl(loggedUser)
UserSearchParams userSearchParams = UserSearchParams.builder().allowEmptyQuery(true).includeActive(true).includeInactive(true).ignorePermissionCheck(true).build()

def rowCount
def rowData
def firstName
def lastName
def email
def displayName
def userFound
def addUser

String userListFile = new File('/atlassian/jira/data/tmp/users-ald.csv').getText()

// JIRA vs CSV - Users re/de-activation
log.debug("JIRA vs CSV")

//for (ApplicationUser user : userManager.getAllApplicationUsers()) {
//for (ApplicationUser user : userSearchService.findUsersAllowEmptyQuery(serviceContext, "")) {
for (ApplicationUser user : userSearchService.findUsers(serviceContext, "", userSearchParams)) {
    log.debug "${user.getName()}"
    rowCount = 0
    userFound = false
    userActive = true
    if (!user.getName().equals("valiantys")) {
        for (String line : userListFile.readLines()) {
            if (rowCount > 0) {
                rowData = line.split("\",\"")            
                email = rowData[3]
            	email = email.replace("\"","")
				activeUser = rowData[14]
                activeUser = activeUser.replace("\"","")
				
                if (user.getEmailAddress().equals(email) && activeUser == 'True') {
                    userFound = true
                    log.debug "${user.getName()} found..."
                }
				if (user.getEmailAddress().equals(email) && activeUser == 'False') {
                    userActive = false
                    log.debug "${user.getName()} inactive..."
                }
            }
            rowCount++
        }
        
        //Re-activate an user found in the file
        if (userFound && userActive && !user.isActive()) {
            UserWithAttributes usr = crowdService.getUserWithAttributes(user.getName())
            updateUser = ApplicationUsers.from(ImmutableUser.newUser(usr).active(true).toUser())
            updateUserValidationResult = userService.validateUpdateUser(updateUser)
            if (updateUserValidationResult.isValid()) {
                userService.updateUser(updateUserValidationResult)
                log.debug "${updateUser.name} reactivated..."
            } else {
                log.error "Update of ${usr.name} failed: ${updateUserValidationResult.getErrorCollection().getErrors().entrySet().join(',')}"
            }
        }

        //De-activate a user not active in the file
        if ( !userActive && user.isActive()) {
            UserWithAttributes usr = crowdService.getUserWithAttributes(user.getName())
            updateUser = ApplicationUsers.from(ImmutableUser.newUser(usr).active(false).toUser())
            updateUserValidationResult = userService.validateUpdateUser(updateUser)
            if (updateUserValidationResult.isValid()) {
                userService.updateUser(updateUserValidationResult)
                log.debug "${updateUser.name} deactivated..."
            } else {
                log.error "Update of ${usr.name} failed: ${updateUserValidationResult.getErrorCollection().getErrors().entrySet().join(',')}"
            }
        }
    }
}

// CSV vs JIRA - Create new users
rowCount = 0
log.debug("CSV vs JIRA")

for (String line : userListFile.readLines()) {    
    if (rowCount > 0) {
        rowData = line.split(",")
        firstName = rowData[0]
        lastName = rowData[1]
        username = rowData[2]
        email = rowData[3]
        activeUser = rowData[14]
		firstName = firstName.replace("\"","")
        lastName = lastName.replace("\"","")
        username = username.replace("\"","")
        email = email.replace("\"","")
		activeUser = activeUser.replace("\"","")
				
        displayName = firstName+" "+lastName
        if (activeUser == 'True') { 
        	addUser = true
		} 
        else { 
            addUser = false 
        }
        
        log.debug "${displayName}"
        
        //for (ApplicationUser user : userManager.getAllApplicationUsers()) {
        for (ApplicationUser user : userSearchService.findUsers(serviceContext, "", userSearchParams)) {
            if (user.getEmailAddress().equals(email)) {
                addUser = false
                log.debug "${displayName} already exists..."
            }
        }
       
        if (addUser) {
			UserRequest = CreateUserRequest.withUserDetails(loggedUser, username, "jira", email, displayName)
			UserRequest.sendNotification(false)
			createUserValidationResult = userService.validateCreateUser(UserRequest)
			// createUserValidationResult = userService.validateCreateUser(UserService.CreateUserRequest.withUserDetails(loggedUser, username, "jira", email, displayName))
            if (createUserValidationResult.isValid()) {
                userService.createUser(createUserValidationResult)
               log.debug "${displayName} created..."
            } else {
                log.error "Creation of ${displayName} ${email} failed: ${createUserValidationResult.getErrorCollection().getErrors().entrySet().join(',')}"
            }
        }
    }
    rowCount++
}