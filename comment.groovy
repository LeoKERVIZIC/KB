import groovy.json.*

def jSlurper = new JsonSlurper()

def directory = '/atlassian/jira/data/tmp/'
def project = 'AN'

def sourceFile = new File( directory + project +'_comments.json').getText('UTF-8')
    
def targetFile = new File( directory + project +'_comment.csv')
targetFile.append("Key;Summary;Comment")

def issueParser = jSlurper.parseText(sourceFile)
def cmtSourceDate
def cmtDate
def cmtBody
def i
def j

for (i = 0; i < issueParser.total; i++) {
	for (j = 0; j < issueParser.issues[i].fields.comment.total; j++) {
        cmtSourceDate = issueParser.issues[i].fields.comment.comments[j].created
        cmtDate = cmtSourceDate.substring(8,10) + "/" + cmtSourceDate.substring(5,7) + "/" + cmtSourceDate.substring(0,4) + " " + cmtSourceDate.substring(11,16)
        cmtBody = issueParser.issues[i].fields.comment.comments[j].body.replaceAll('"','\'')
        targetFile.append('\n"' + issueParser.issues[i].key + '";"' + issueParser.issues[i].fields.summary.replaceAll('"',"'") + '";"' + cmtDate  + ';' + issueParser.issues[i].fields.comment.comments[j].author.name + ';' + cmtBody + '"') 
    }
}