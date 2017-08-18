#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, json, io, sys, urllib
from HTMLParser import HTMLParser
from datetime import datetime

keysToRemove = ["done_status_date", "user_02_s", "user_03_s", "user_05_d", "user_03_d", "detected_in_sprint", "user_14_s", "user_12_s", "user_11_s", "user_07_s", "user_08_d", "pending_acceptance_tests", "passed_acceptance_tests", "user_04_s", "archive_status", "application_id", "rank", "cover_status", "failed_acceptance_tests", "kanban_status_id", "estimated", "kanban_parent_status_HP AGM ID", "kanban_parent_status_id", "blocked", "actual", "kan_parent_duration", "invested", "HP AGM ID", "kan_status_duration", "dev_comments", "estimate", "remaining", "num_of_defects","num_of_user_stories", "status_duration", "wsjf_job_size", "user_10", "initial_estimate", "wsjf_risk", "wsjf_user_impact", "user_13", "wsjf_cod", "applications", "agg_story_points", "wsjf_time_effort", "owner", "wsjf", "agg_bli_story_points", "defect_priority", "defect_status", "user_04_d", "user_06_d", "user_07_d", "user_09_d", "user_11_d", "detected_in_rel", "severity", "fixed_on_date", "detection_date", "closing_date", "user_01_d", "detected_by", "user_02_d"]

#

blankKeys = []
idsToSearchForTasks = []
releaseIds = []
issueLinks = []
namesNotFound = []
status = []

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

with open('usernameids.json') as data_file:
    usernameids = json.load(data_file)

print "Please enter the ID for the application you wish to download"
application_id = int(raw_input())

print "Please enter the Project Key to be used in JIRA"
projectKey = raw_input().upper()

print "Please enter the Project Admin (X/A...) to be used in JIRA"
projectAdmin = raw_input().upper()

print "Export Teams Y/[N]"
teamExport = raw_input().upper()

print "Export Sprints Y/[N]"
sprintExport = raw_input().upper()


print "Load Users\n"
with open('users.json') as data_file:
    user_data = json.load(data_file)

userList = []

for user in user_data:
    newUser = {"name" : user["name"],
        "fullname" : user["fullname"],
        "email" : user["email"],
        "groups" : ["jira-software-users"],
        "active": True}
    userList.append(newUser)
    
def featureNameLookup(featureId, featuresList):
    for feature in featuresList:
        if feature["externalId"] == featureId:
            return feature["summary"]
    return ""

def jiraifyKeys(obj, featuresList):
    customFieldValuesToAdd = list()
    
    for key in obj.keys():
        if key in keysToRemove:
            del obj[key]
        #elif (key in blankKeys) and (obj[key] is not None):
        #    if obj[key] is not None:
                #print "Key: " + str(key)
        #    del obj[key]
        else:
            if key == "description":
                if obj[key] != None:
                    obj[key] = strip_tags(obj[key])
                    obj[key] = unicode(obj[key])
            if key == "name":
                new_key = "summary"
                obj[new_key] = obj[key]
                obj[new_key] = unicode(obj[new_key])
                del obj[key]
            if key == "author":
                new_key = "reporter"
                if obj[key] == "":
                    obj["reporter"] = obj[key]
                else:
                    keyString = str(obj[key])
                    if usernameids.has_key(keyString):
                        obj["reporter"] = usernameids[keyString]   
                    else:
                        obj["reporter"] = projectAdmin
                        namesNotFound.append(obj[key])
                del obj[key]
            if key == "theme_type":
                customFieldValuesToAdd.append({"fieldName": "Initiative Type", "fieldType": "com.atlassian.jira.plugin.system.customfieldtypes:select", "searcherType": "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher", "value": obj["theme_type"]})
                del obj[key]
            if key in ("feature_type", "type", "issueType"):
                new_key = "issueType"
                obj[new_key] = obj[key]
                if obj[new_key] == "theme":
                    obj[new_key] = "Initiative"
                if obj[new_key] == "task":
                    obj[new_key] = "Sub-task"
                    obj["summary"] = obj["description"]
                if obj[new_key] == "backlog_item":
                    if obj["subtype"] == "defect":
                        obj[new_key] = "Bug"
                    else:
                        obj[new_key] = "Story"
                    del obj["subtype"]
                if obj[new_key] == "feature" or obj[new_key] == "Epic":
                    obj[new_key] = "Epic"
                    if obj.has_key("summary"):
                        customFieldValuesToAdd.append({"fieldName": "Epic Name", "fieldType": "com.pyxis.greenhopper.jira:gh-epic-label", "searcherType": "com.pyxis.greenhopper.jira:gh-epic-label-searcher", "value": obj["summary"]})
                    if obj.has_key("name"):
                        customFieldValuesToAdd.append({"fieldName": "Epic Name", "fieldType": "com.pyxis.greenhopper.jira:gh-epic-label", "searcherType": "com.pyxis.greenhopper.jira:gh-epic-label-searcher", "value": obj["name"]})
                del obj[key]
            if key == "creation_date":
                new_key = "created"
                obj[new_key] = obj[key]
                del obj[key]
            if key == "feature_id":
                if obj[key] is not None:
                    featureName = featureNameLookup(obj[key]["id"], featuresList)
                    newValue = {"fieldName": "Epic Link", "fieldType": "com.pyxis.greenhopper.jira:gh-epic-link", "value": featureName}
                    customFieldValuesToAdd.append(newValue)
                del obj[key]
            if key == "last_modified":
                new_key = "updated"
                obj[new_key] = obj[key]
                del obj[key]
            if key == "story_priority":
                new_key = "priority"
                obj[new_key] = obj[key]
                del obj[key]
            if key == "id":
                new_key = "externalId"
                obj[new_key] = obj[key]
                if obj.has_key("item_id"):
                    
#                    if obj["item_id"] == 42385:
                    idPair = {}
                    idPair["key"] = obj["item_id"]
                    idPair["externalId"] = obj["externalId"]
                        
#                        print "\nid pair : id = " + str(idPair["key"]) + " ; external id = " + str(idPair["externalId"]) + "\n"
                        
                    with open("idpair.json", "a") as idPairFile:
                        idPairFile.write(unicode(json.dumps(idPair, ensure_ascii=True))+", ")
                    
                    obj[key] = obj["item_id"]                    
                    del obj["item_id"]
                obj["key"] = projectKey + "-" + str(obj[key])
                del obj[key]
            if key == "assigned_to":
                new_key = "assignee"
                if obj[key] == "":
                    obj[new_key] = obj[key]
                else:
                    keyString = str(obj[key])
                    if usernameids.has_key(keyString):
                        obj[new_key] = usernameids[keyString] 
                    else:
                        obj[new_key] = projectAdmin
                        namesNotFound.append(obj[key])
                    del obj[key]
            if key == "num_of_tasks":
                if obj.has_key("id"):
                    if obj["id"] == 52407:
                        print str(obj)
                if obj.has_key("item_id"):
                    if obj["item_id"] == 54320:
                        print str(obj)
                if obj[key] is not None:
                    if obj[key] > 0:
                        if obj.has_key("externalId"):
                            idsToSearchForTasks.append(obj["externalId"])
                        elif obj.has_key("id"):
                            idsToSearchForTasks.append(obj["id"])
                        else:
                            print "tasks to link, but no id"
                            print str(obj)
                del obj[key]
            if key == "release_id":
                if obj[key] is not None:
                    releaseIds.append(obj[key]["id"])
                else:
                    del obj[key]
            if key == "theme_id":
                if obj[key] is not None:
                    theme_key = projectKey + "-" + str(obj["theme_id"]["id"])
                    customFieldValuesToAdd.append({"fieldName": "Parent Link", "fieldType": "com.atlassian.jpo:jpo-custom-field-parent", "searcherType": "com.atlassian.jpo:jpo-custom-field-parent-searcher", "value": theme_key})
                del obj[key]
            if key == "remaining":
                new_key = "estimate"
                obj[new_key] = obj[key]
                del obj[key]
            if key == "backlog_item_id":
                if obj[key]["id"] == 52407:
                    print str(obj)
                createAndAddLink(obj[key]["id"], obj["id"], "sub-task-link")
                del obj[key]
            if key == "story_points" or key == "Story Points":
                storyKeyValue = obj[key]
                if storyKeyValue is not None:
                    newValue =  {"fieldName": "Story Points", "fieldType": "com.atlassian.jira.plugin.system.customfieldtypes:float", "searcherType": "com.atlassian.jira.plugin.system.customfieldtypes:exactnumber", "value" : obj[key]}
                    customFieldValuesToAdd.append(newValue)
                del obj[key]
            obj["customFieldValues"] = customFieldValuesToAdd
# For setting the Item Readiness Status 2 field in Jira
            if key == "user_03":
                storyKeyValue = obj[key]
                if storyKeyValue is not None:
                    newValue =  {"fieldName": "Item Readiness Status 2", "fieldType": "com.atlassian.jira.plugin.system.customfieldtypes:labels", "searcherType": "com.atlassian.jira.plugin.system.customfieldtypes:labelsearcher", "value" : obj[key]}
                    customFieldValuesToAdd.append(newValue)
                del obj[key]
            obj["customFieldValues"] = customFieldValuesToAdd
# For setting the Item Readiness Status field in Jira
            if key == "user_02":
                storyKeyValue = obj[key]
                if storyKeyValue is not None:
                    itemReadinessStatus = ''
                    for value in obj[key]:
                        itemReadinessStatus = itemReadinessStatus + value + ';'
                    itemReadinessStatus = itemReadinessStatus[:-1]
                    newValue =  {"fieldName": "Item Readiness Status", "fieldType": "com.atlassian.jira.plugin.system.customfieldtypes:labels", "searcherType": "com.atlassian.jira.plugin.system.customfieldtypes:labelsearcher", "value" : itemReadinessStatus.replace(' ', '_')}
                    customFieldValuesToAdd.append(newValue)
                del obj[key]
            obj["customFieldValues"] = customFieldValuesToAdd
# For setting the Environment field in Jira
            if key == "user_01":
                storyKeyValue = obj[key]
                if storyKeyValue is not None:
                    obj[key] = obj[key].replace(" ", "_")
                    newValue =  {"fieldName": "Environment Name", "fieldType": "com.atlassian.jira.plugin.system.customfieldtypes:labels", "searcherType": "com.atlassian.jira.plugin.system.customfieldtypes:labelsearcher", "value" : obj[key]}
                    customFieldValuesToAdd.append(newValue)
                del obj[key]
            obj["customFieldValues"] = customFieldValuesToAdd
# For setting the Team field in Jira
            if key == "team_id":
                if obj[key] is not None:
#                    print obj[key]
#                    print 'team id : ' + str(obj[key]["id"])
                    teamName = teamNameFunction(obj[key]["id"])
#                    print 'team name : ' + teamName
#                    raw_input()
                    if teamName is not None:
                        teamName = teamName.replace(' ', '_')
                        newValue =  {"fieldName": "Team", "fieldType": "com.atlassian.jira.plugin.system.customfieldtypes:labels", "searcherType": "com.atlassian.jira.plugin.system.customfieldtypes:labelsearcher", "value" : teamName}
                        customFieldValuesToAdd.append(newValue)
                del obj[key]
            obj["customFieldValues"] = customFieldValuesToAdd
# For setting the Sprint field in Jira
            if key == "sprint_id":
                if obj[key] is not None:
                    sprintName = sprintNameFunction(obj[key]["id"])
                    if sprintName is not None:
                        sprintName = sprintName.replace(' ', '_')
                        labelsList = list()
                        labelsList.append(sprintName)
                        obj["labels"] = labelsList
                del obj[key]
# For setting the Due Date field in Jira
            if key == "user_05_s":
                    new_key = "duedate"
                    obj[new_key] = obj[key]
                    del obj[key]
# For setting the Scheduled/Deliver Date field in Jira
            if key == "user_01_s":
                storyKeyValue = obj[key]
                if storyKeyValue is not None:
                    d = datetime.strptime(obj[key], '%Y-%m-%d')
                    day_string = d.strftime('%d/%b/%y')
                    newValue =  {"fieldName": "Scheduled/Delivered Date", "fieldType": "com.atlassian.jira.plugin.system.customfieldtypes:datepicker", "searcherType": "com.atlassian.jira.plugin.system.customfieldtypes:daterange", "value" : day_string}
                    customFieldValuesToAdd.append(newValue)
                del obj[key]
            obj["customFieldValues"] = customFieldValuesToAdd
# For setting the Client Entity field in Jira
            if key == "user_09_s":
                storyKeyValue = obj[key]
                if storyKeyValue is not None:
                    newValue =  {"fieldName": "Client Entity", "fieldType": "com.atlassian.jira.plugin.system.customfieldtypes:multiselect", "searcherType": "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher", "value" : obj[key]}
                    customFieldValuesToAdd.append(newValue)
                del obj[key]
            obj["customFieldValues"] = customFieldValuesToAdd
# For setting the Customer Commitment Form Reference field in Jira
            if key == "user_06_s":
                storyKeyValue = obj[key]
                if storyKeyValue is not None:
                    newValue =  {"fieldName": "Customer Commitment form Reference", "fieldType": "com.atlassian.jira.plugin.system.customfieldtypes:textfield", "searcherType": "com.atlassian.jira.plugin.system.customfieldtypes:textsearcher", "value" : obj[key]}
                    customFieldValuesToAdd.append(newValue)
                del obj[key]
            obj["customFieldValues"] = customFieldValuesToAdd
# For setting the Release Train field in Jira
            if key == "user_08_s":
                storyKeyValue = obj[key]
                if storyKeyValue is not None:
                    newValue =  {"fieldName": "Release train", "fieldType": "com.atlassian.jira.plugin.system.customfieldtypes:labels", "searcherType": "com.atlassian.jira.plugin.system.customfieldtypes:labelsearcher", "value" : obj[key].replace(' ', '_')}
                    customFieldValuesToAdd.append(newValue)
                del obj[key]
            obj["customFieldValues"] = customFieldValuesToAdd
# For setting the resolution field in Jira
            if key == "status":
                status.append(obj[key])
                if obj[key] == "Done" or obj[key] == "Completed":
                    obj["resolution"] = "Done"
                    obj["resolutionDate"] = obj["last_modified"] #or "updated" to check

    if "author" not in obj.keys():
        obj["reporter"] = projectAdmin
    return obj

loadFromDiskOrLive = "Live"

if (loadFromDiskOrLive == "Disk"):
    with open('data.json') as data_file:
        data = json.load(data_file)
        issuesList = data["projects"][0]["issues"]
        for issue in issuesList:
            jiraifyKeys(issue, None)
        with io.open('data.json', 'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(data, ensure_ascii=False)))
    sys.exit()

def loginFunction():
    url = 'https://agilemanager-lon.saas.hp.com/agm/oauth/token'
    payload = 'client_id=api_client_739146427_3&client_secret=4mdvOAgs3lt7uG2&grant_type=client_credentials'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, data=payload, headers=headers)

    #collect token
    #Use token for rest of the requests.

    jsonDump = json.loads(r.text)
    access_token = jsonDump['access_token']
    return jsonDump['access_token']

def backlog_itemsFunction(access_token):
    numberOfPasses = 0
    offset = 0
    currentResults = 0
    bearer = 'bearer ' + access_token
    url = 'https://agilemanager-lon.saas.hp.com/agm/api/workspaces/1000/backlog_items?query=%22application_id%3D' + str(application_id) + '%22&&&offset=' + str(offset)
    headers = {'Content-Type': 'application/json', 'Authorization': bearer}
    r = requests.get(url, headers=headers)
    backLogItemsDump = json.loads(r.text)
    totalResults = backLogItemsDump['TotalResults']
    currentResults = currentResults + len(backLogItemsDump['data'])
    backlog_items = backLogItemsDump['data']
    print 'Backlog Application Pass number ' + str(numberOfPasses) + ' : 0 - 100 -> ' + str(totalResults) + ' in total'
    
    while totalResults > currentResults: 
        offset = offset + 100
        numberOfPasses = numberOfPasses + 1
        print 'Backlog Application Pass number ' + str(numberOfPasses) + ' : ' + str(offset) + ' - ' + str(offset + 100)
        offsetUrl = 'https://agilemanager-lon.saas.hp.com/agm/api/workspaces/1000/backlog_items?query=%22application_id%3D' + str(application_id) + '%22&&&offset=' + str(offset)
        offsetR = requests.get(offsetUrl, headers=headers)
        offsetBackLogItemsDump = json.loads(offsetR.text)
        currentResults = currentResults + len(offsetBackLogItemsDump['data'])
        new_backlog_items = offsetBackLogItemsDump['data']
        backlog_items = backlog_items + new_backlog_items
    
    print '\nBacklog Application results to keep: ' + str(len(backlog_items)) + '\n'
    print '######\n'
    return backlog_items

def featuresFunction(access_token, themeIds, featureIds):
    numberOfPasses = 0
    
    offset = 0
    currentResults = 0
    bearer = 'bearer ' + access_token
    url = 'https://agilemanager-lon.saas.hp.com/agm/api/workspaces/1000/features'
    headers = {'Content-Type': 'application/json', 'Authorization': bearer}
    queryString = '"theme_id='
    themeIds = list(set(themeIds))
    numberOfThemes = len(themeIds)
    if len(themeIds) != 0: #If there are Themes
        for id in themeIds:
    #Specific for DDD project        if (id != 1178) and (id !=1180):
                queryString = queryString + str(id) + '||theme_id='
        else:
            queryString = queryString[:-11] + '"'
    #Initial code, above code is corrected        queryString = queryString + str(id) + '"'
        payload = "?query=" + urllib.quote_plus(queryString) + '&offset=' + str(offset)
        url2 = url + payload
    #Debug    print url2
        r = requests.get(url2, headers=headers)
        featuresDump = json.loads(r.text)
        totalResults = featuresDump['TotalResults']
        currentResults = currentResults + len(featuresDump['data'])
        features = featuresDump['data']
        print 'Features from Theme Pass number ' + str(numberOfPasses) + ' : 0 - 100 -> ' + str(len(features)) + ' in total'
        
        while totalResults > currentResults: 
            numberOfPasses = numberOfPasses + 1
            print 'Features from Theme Pass number ' + str(numberOfPasses) + ' : ' + str(offset) + ' / ' + str(offset + 100)
            payload = "?query=" + urllib.quote_plus(queryString) + '&offset=' + str(offset)
            url2 = url + payload
    #Debug        print url2
            r = requests.get(url2, headers=headers)
            offsetFeaturesDump = json.loads(r.text)
            offset = currentResults
            currentResults = currentResults + len(offsetFeaturesDump['data'])
            new_features = offsetFeaturesDump['data']
            features = features + new_features
            
        print 'Features from Themes results: ' + str(len(features))
    else:
        print 'Features from Theme Pass number ' + str(numberOfPasses) + ' : 0 - 100 -> 0 in total'

    numberOfPasses = 0
    url = 'https://agilemanager-lon.saas.hp.com/agm/api/workspaces/1000/features'
    headers = {'Content-Type': 'application/json', 'Authorization': bearer}
    queryString = '"id='
    featureIds = list(set(featureIds))
    numberOfThemes = len(featureIds)
    for id in featureIds:
        queryString = queryString + str(id) + '||id='
    else:
        queryString = queryString + str(id) + '"'
    payload = "?query=" + urllib.quote_plus(queryString) + '&offset=' + str(offset)
    url2 = url + payload
    r = requests.get(url2, headers=headers)
    featuresDump = json.loads(r.text)
    totalResults = featuresDump['TotalResults']
    
    print '\nFeatures Pass number ' + str(numberOfPasses) + ' : 0 - 100 -> ' + str(totalResults) + ' in total'
    
    currentResults = currentResults + len(featuresDump['data'])
    if len(themeIds) != 0: #If there are Themes
        features = features + featuresDump['data']
    else: #If there are no Themes
        features = featuresDump['data']
    
    print 'Features  results: ' + str(totalResults)
    while totalResults > currentResults: 
        numberOfPasses = numberOfPasses + 1
        print 'Features Pass number ' + str(numberOfPasses) + " : " + str(offset - 100) + " - " + str(offset)
        payload = "?query=" + urllib.quote_plus(queryString) + '&offset=' + str(offset)
        url2 = url + payload
        r = requests.get(url2, headers=headers)
        offsetFeaturesDump = json.loads(r.text)
        offset = currentResults
        currentResults = currentResults + len(offsetFeaturesDump['data'])
        new_features = offsetFeaturesDump['data']
        features = features + new_features

    print '\nFeatures total results ' + str(len(features))
    return features

def themesFunction(access_token, applicationId):
    print '\n######\n'
    themesToKeep = list()
    numberOfPasses = 0
    offset = 0
    currentResults = 0
    bearer = 'bearer ' + access_token
    url = 'https://agilemanager-lon.saas.hp.com/agm/api/workspaces/1000/themes?offset=' + str(offset) + '&'
    headers = {'Content-Type': 'application/json', 'Authorization': bearer}
    r = requests.get(url, headers=headers)
    themesDump = json.loads(r.text)
    totalResults = themesDump['TotalResults']
    currentResults = currentResults + len(themesDump['data'])
    themes = themesDump['data']
    applicationIdData = {'type':'application', 'id':applicationId}
    print 'Themes Pass number ' + str(numberOfPasses) + ' : 0 - 100 -> ' + str(totalResults) + ' in total'
    
    while totalResults > currentResults: 
        offset = offset + 100
        numberOfPasses = numberOfPasses + 1
        print 'Themes Pass number ' + str(numberOfPasses) + ' : ' + str(offset) + " - " + str(offset + 100)
        offsetUrl = 'https://agilemanager-lon.saas.hp.com/agm/api/workspaces/1000/themes?offset=' + str(offset) + '&'
        offsetR = requests.get(offsetUrl, headers=headers)
        offsetThemesDump = json.loads(offsetR.text)
        currentResults = currentResults + len(offsetThemesDump['data'])
        new_themes = offsetThemesDump['data']
        themes = themes + new_themes
        

    print '\nThemes total results: ' + str(len(themes))

    for individualTheme in themes:
        themeApplications = individualTheme['applications']['data']
        if applicationIdData in themeApplications:
            themesToKeep.append(individualTheme)
        pass
    print '\nThemes results to keep ' + str(len(themesToKeep)) + '\n'
    print '######\n'
    return themesToKeep

def teamNameFunction(teamId):
    for team in teamList:
        if team["id"] == teamId:
            return team["name"]
    
def teamFunction(access_token):
    numberOfPasses = 0
    offset = 0
    currentResults = 0
    bearer = 'bearer ' + access_token
    url = 'https://agilemanager-lon.saas.hp.com/agm/api/workspaces/1000/teams?offset=' + str(offset) + '&'
    headers = {'Content-Type': 'application/json', 'Authorization': bearer}
    r = requests.get(url, headers=headers)
    teamsDump = json.loads(r.text)
    totalResults = teamsDump['TotalResults']
    currentResults = currentResults + len(teamsDump['data'])
    teams = teamsDump['data']
    print 'Teams Pass number ' + str(numberOfPasses) + ' : 0 - 100 -> ' + str(totalResults) + ' in total'
    
    while totalResults > currentResults: 
        offset = offset + 100
        numberOfPasses = numberOfPasses + 1
        print 'Teams Pass number ' + str(numberOfPasses) + ' : ' + str(offset) + " - " + str(offset + 100)
        offsetUrl = 'https://agilemanager-lon.saas.hp.com/agm/api/workspaces/1000/teams?offset=' + str(offset) + '&'
        offsetR = requests.get(offsetUrl, headers=headers)
        offsetteamsDump = json.loads(offsetR.text)
        currentResults = currentResults + len(offsetteamsDump['data'])
        new_teams = offsetteamsDump['data']
        teams = teams + new_teams
    
    print '\nTeams total results: ' + str(len(teams))
    
    return teams

def sprintNameFunction(sprintId):
    for sprint in sprintList:
        if sprint["id"] == sprintId:
            return sprint["name"]
    
def sprintFunction(access_token):
    numberOfPasses = 0
    offset = 0
    currentResults = 0
    bearer = 'bearer ' + access_token
    url = 'https://agilemanager-lon.saas.hp.com/agm/api/workspaces/1000/sprints?offset=' + str(offset) + '&'
    headers = {'Content-Type': 'application/json', 'Authorization': bearer}
    r = requests.get(url, headers=headers)
    sprintDump = json.loads(r.text)
    totalResults = sprintDump['TotalResults']
    currentResults = currentResults + len(sprintDump['data'])
    sprint = sprintDump['data']
    print 'Sprints Pass number ' + str(numberOfPasses) + ' : 0 - 100 -> ' + str(totalResults) + ' in total'
    
    while totalResults > currentResults: 
        offset = offset + 100
        numberOfPasses = numberOfPasses + 1
        print 'Sprints Pass number ' + str(numberOfPasses) + ' : ' + str(offset) + " - " + str(offset + 100)
        offsetUrl = 'https://agilemanager-lon.saas.hp.com/agm/api/workspaces/1000/sprints?offset=' + str(offset) + '&'
        offsetR = requests.get(offsetUrl, headers=headers)
        offsetsprintDump = json.loads(offsetR.text)
        currentResults = currentResults + len(offsetsprintDump['data'])
        new_sprint = offsetsprintDump['data']
        sprint = sprint + new_sprint
    
    print '\nSprints total results: ' + str(len(sprint))
    
    return sprint
    
def searchForExistingSummary(summary, features):
    return [element for element in features if element['name'].lower() == summary.lower()]

def searchForExistingKey(id, features):
    return [element for element in features if element['id'] == id]

def createAndAddLink(parentId, childId, linkType):
    
#    with open('idpair.json') as data_file:
#        id_data = json.load(data_file)
#    id_dataList = []
#    for id in id_data:
#        id_dataList.append(id)
#        
#    for pair in id_dataList:
#        if parentId == 48686:
#                print "destinationId : " + str(parentId) + " ; sourceId : " + str(childId)
#                print "externalId : " + str(pair["externalId"]) + " ; key : " + str(pair["key"])
#        if pair["externalId"] == parentId:
#            parentId = pair["key"]
    
    linkToAdd = {"name": linkType,
    "sourceId": childId,
    "destinationId": parentId}
    issueLinks.append(linkToAdd)
    return None

def tasksFunction(access_token, listOfBacklogItemIds):
    numberOfPasses = 0
    offset = 0
    currentResults = 0
    bearer = 'bearer ' + access_token
    url = 'https://agilemanager-lon.saas.hp.com/agm/api/workspaces/1000/tasks'
    headers = {'Content-Type': 'application/json', 'Authorization': bearer}
    queryString = '"backlog_item_id='
    for id in listOfBacklogItemIds:
        queryString = queryString + str(id) + '||backlog_item_id='
    else:
#        queryString = queryString + '7679"'
        queryString = queryString[:-18]
        queryString = queryString + '"'
    payload = "?query=" + urllib.quote_plus(queryString) 
    url = url + payload + '&offset='
    urlToUse = url + str(offset)
    r = requests.get(urlToUse, headers=headers)
    tasksDump = json.loads(r.text)
    totalResults = tasksDump['TotalResults']
    currentResults = currentResults + len(tasksDump['data'])
    tasksList = tasksDump['data']
    
    while totalResults > currentResults: 
        offset = offset + 100
        numberOfPasses = numberOfPasses + 1
        offsetUrl = url + str(offset)
        offsetR = requests.get(offsetUrl, headers=headers)
        offsettasksDump = json.loads(offsetR.text)
        currentResults = currentResults + len(offsettasksDump['data'])
        new_tasksList = offsettasksDump['data']
        tasksList = tasksList + new_tasksList
    
    print 'Tasks results to keep ' + str(len(tasksList))
    
    return tasksList

def releasesFunction(access_token, listOfReleaseIds):
    numberOfPasses = 0
    print 'Releases Pass number: ' + str(numberOfPasses)
    offset = 0
    currentResults = 0
    bearer = 'bearer ' + access_token
    url = 'https://agilemanager-lon.saas.hp.com/agm/api/workspaces/1000/releases'
    headers = {'Content-Type': 'application/json', 'Authorization': bearer}
    queryString = '"id='
    for id in listOfReleaseIds:
        queryString = queryString + str(id) + '||id='
    else:
        queryString = queryString + str(id) + '"'
    payload = "?query=" + urllib.quote_plus(queryString) 
    url = url + payload + '&offset='
    urlToUse = url + str(offset)
    r = requests.get(urlToUse, headers=headers)
    releasesDump = json.loads(r.text)
    totalResults = releasesDump['TotalResults']
    currentResults = currentResults + len(releasesDump['data'])
    releasesList = releasesDump['data']

    while totalResults > currentResults: 
        offset = offset + 100
        numberOfPasses = numberOfPasses + 1
        print 'Releases Pass number: ' + str(numberOfPasses) + 'Total results: ' + str(totalResults)
        offsetUrl = url + str(offset)
        offsetR = requests.get(offsetUrl, headers=headers)
        offsetReleasesDump = json.loads(offsetR.text)
        currentResults = currentResults + len(offsetReleasesDump['data'])
        new_releasesList = offsetReleasesDump['data']
        releasesList = releasesList + new_releasesList

    return releasesList

def createVersions(versionsList):
    versions = []
    for version in versionsList:
        released = True
        if version["active"] == "Y":
            released = False
        releaseDescription = ""
        if version["description"] != None:
            releaseDescription = strip_tags(version["description"])
        newVersion = {"name" : version["name"],
        "released" : released,
      "archived" : False,
      "releaseDate" : version["end_date"],
      "description": releaseDescription}
        newVersion["id"] = version["id"]
        versions.append(newVersion)
    return versions

def updateVersions(issueList, versionsList):

    for issue in issueList:
        if issue.has_key("release_id"):
            fixedVersionsList = []
            versionId = issue["release_id"]["id"]
            for version in versionsList:
                if str(versionId) == str(version["id"]):
                    fixedVersionsList.append(version["name"])
            issue["fixedVersions"] = fixedVersionsList
            del issue["release_id"]

print '\n######\n'
print 'Login'
print '\n######\n'
access_token = loginFunction()

print "Load Teams\n"
if teamExport == "Y":
    teamList = teamFunction(access_token)
    f = open('teams.json', 'w')
    with io.open('teams.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(teamList, ensure_ascii=True)))
    f.close()
else:
    with open('teams.json') as data_file:
        team_data = json.load(data_file)
    teamList = []
    for team in team_data:
        newTeam = {"name" : team["name"], "id" : team["id"]}
        teamList.append(newTeam)

print '\n######\n'
print "Load Sprints\n"
if sprintExport == "Y" or sprintExport == "y":
    sprintList = sprintFunction(access_token)
    with io.open('sprints.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(sprintList, ensure_ascii=True)))
    f.close()
else:
    with open('sprints.json') as data_file:
        sprint_data = json.load(data_file)
    sprintList = []
    for sprint in sprint_data:
        sprintList.append(sprint)

with open("idpair.json", "w") as idPairFile:
    idPairFile.write("[")


themes = themesFunction(access_token, application_id)

listOfThemeIds = [d['id'] for d in themes]

tempThemes =[]

for theme in themes:
    jiraifyKeys(theme, None)
    if theme not in tempThemes:
        tempThemes.append(theme)        
themes = tempThemes

backlogData = backlog_itemsFunction(access_token)
featureIdsToAdd = list()
for backlogItemId in backlogData:
    if backlogItemId["feature_id"] is not None:
        featureIdsToAdd.append(backlogItemId["feature_id"]["id"])

features = featuresFunction(access_token, listOfThemeIds, featureIdsToAdd)

tmp=[]

xxx = 1
for feature in features:
    if feature not in tmp:
        if (searchForExistingSummary(feature["name"], tmp)):
                feature["name"] = feature["name"] + "-0" + str(xxx)
                xxx = xxx + 1
        if not (searchForExistingKey(feature["id"], tmp)):
            tmp.append(feature)

features = tmp
for feature in features:
    jiraifyKeys(feature, features)

print 'Features results to keep: ' + str(len(features))
print '\n#####\n'

for backlogItem in backlogData:
    jiraifyKeys(backlogItem, features)

with open("idpair.json", "r") as idPairFile:
    data = idPairFile.read()
    data = data[:-2]
    idPairFile.close()
with open("idpair.json", "w") as idPairFile:
    idPairFile.write(data + "]")

tasks = []

idsToSearchForTasks = list(set(idsToSearchForTasks))
taskRuns = 0
numberOfIDsAtOnce = 40
totalRequiredPasses = float(len(idsToSearchForTasks)) / float(numberOfIDsAtOnce)
totalRequiredPasses = int(totalRequiredPasses) + 1
# while len(idsToSearchForTasks) >= numberOfIDsAtOnce:
while taskRuns < totalRequiredPasses:
    taskRuns = taskRuns + 1
    print 'Tasks Pass number ' + str(taskRuns)
    tasks = tasks + tasksFunction(access_token, idsToSearchForTasks[0:numberOfIDsAtOnce])
    del idsToSearchForTasks[0:numberOfIDsAtOnce]

    pass

for task in tasks:
    jiraifyKeys(task, features)

print '\nTasks results to keep: ' + str(len(tasks))
print '\n#####\n'

issueData = themes + features + backlogData + tasks
print 'Total issue results: ' + str(len(issueData)) + '\n'

releaseIds = list(set(releaseIds))

releases = releasesFunction(access_token, releaseIds)
versions = createVersions(releases)
updateVersions(issueData, versions)

finalExportData = {
    "users": userList,
    "links": issueLinks,
    "projects": [{
    "externalName" : projectKey,
    "name" : projectKey,
    "key" : projectKey,
    "lead" : "admin",
    "type" : "software",
    "assigneeType" : 3,
    "issues" : issueData,
    "versions": versions}]
    }

with io.open('data.json', 'w', encoding='utf-8') as f:
    f.write(unicode(json.dumps(finalExportData, ensure_ascii=True)))

#print "Completed with " + str(len(namesNotFound)) + " issues with assignees/reporters not found"
#print "Completed with " + str(len(status)) + " statuses: "
#print '[%s]' % ', '.join(map(str, status))