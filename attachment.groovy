import groovy.json.*

def jSlurper = new JsonSlurper()

def directory = '/atlassian/jira/data/tmp/'
def project = 'FMEL'

def sourceFile = new File( directory + project +'_Attachment.json').getText('UTF-8')
    
def downloadFile = new File( directory + project +'_attachment.sh')

downloadFile.append("#!/bin/sh -e")
downloadFile.append("\nmkdir "+ project)
downloadFile.append("\ncd "+ project)


def targetFile = new File( directory + project +'_attachment.csv')
targetFile.append("Key;Summary;Attachment")

def issueParser = jSlurper.parseText(sourceFile)
def attURL
def attName
def i
def j

for (i = 0; i < issueParser.total; i++) {
	downloadFile.append("\nmkdir " + issueParser.issues[i].key)
	downloadFile.append("\ncd " + issueParser.issues[i].key)

    for (j = 0; j < issueParser.issues[i].fields.attachment.size(); j++) {
        attURL = issueParser.issues[i].fields.attachment[j].content
        attName = issueParser.issues[i].fields.attachment[j].filename.replaceAll(" ","+")
        attName = attName.replaceAll("%27","'")
		attName = attName.replaceAll("%26","&")
		attName = attName.replaceAll("\\s","+")
        
		downloadFile.append("\nmkdir " + issueParser.issues[i].fields.attachment[j].id)
		downloadFile.append("\ncd " + issueParser.issues[i].fields.attachment[j].id)
        downloadFile.append('\ncp /var/atlassian/application-data/jira/tmp/JIRA_EFL/'+ project +'/' + issueParser.issues[i].key + '/' + issueParser.issues[i].fields.attachment[j].id + ' "./' + attName + '"')
		downloadFile.append("\ncd ..")
        
        targetFile.append('\n"' + issueParser.issues[i].key + '";"' + issueParser.issues[i].fields.summary.replaceAll('"',"'") + '";file://'+ project +'/' + issueParser.issues[i].key + '/' +  issueParser.issues[i].fields.attachment[j].id + '/' + attName ) 
    }
	downloadFile.append("\ncd ..")
}