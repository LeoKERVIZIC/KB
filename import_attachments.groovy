import groovy.json.*

def jSlurper = new JsonSlurper()

def sourceFile = new File('C:\\Program Files (x86)\\Atlassian\\JIRA\\temp\\attachments.txt').getText('UTF-8')
    
def downloadFile = new FileC:\\Program Files (x86)\\Atlassian\\JIRA\\temp\\download.bat')
downloadFile.append('\n echo off")

	
def targetFile = new File('C:\\Program Files (x86)\\Atlassian\\JIRA\\temp\\attachments.csv')
targetFile.append("Key;Summary;Attachment;URL")

def issueParser = jSlurper.parseText(sourceFile)
def attURL
def attName
def index
def i
def j

for (i = 0; i < issueParser.total; i++) {
	//downloadFile.append('\n mkdir '+ issueParser.issues[i].key)
	downloadFile.append('\n md '+ issueParser.issues[i].key)
	downloadFile.append('\n cd ' + issueParser.issues[i].key)
		
	for (j = 0; j < issueParser.issues[i].fields.attachment.size(); j++) {
        attURL = issueParser.issues[i].fields.attachment[j].content
        index = attURL.lastIndexOf('/') + 1
        attName = attURL.substring(index)
		
		//downloadFile.append('\n mkdir ' + attFolder)
		downloadFile.append('\n md '+ attFolder)
		downloadFile.append('\n cd ' + attFolder)
		downloadFile.append('\n curl -O -leo.kervizic:Darkmoon09 ' + attURL)
        targetFile.append('\n' + issueParser.issues[i].key + ';' + issueParser.issues[i].fields.summary + ';file://'+ issueParser.issues[i].key + '/' + attFolder + '/' + attName+ ';' + attURL) 
		downloadFile.append('\n cd ..')
	}
	downloadFile.append('\n cd ..')
	
}