#!/usr/bin/env python
import json
import requests

from jira import JIRA

'''

 jira_user:
   state: present
   name: ProjectOne_admin
   passowrd: .ProjectOne
   display_name: 'Hoi Tsang'
   email_address: hoi.h.tsang@gmail.com
   app_keys: ['jira-software']
 register: cmd_jira_user
  
 jira_project:
   state: present
   name: ProjectOne
   summary: "Project One space"
   description: "Project One description"
   assignee: ProjectOne_admin
   view: scrum
'''

'''
{
    "name": "charlie",
    "password": "abracadabra",
    "emailAddress": "charlie@atlassian.com",
    "displayName": "Charlie of Atlassian",
    "applicationKeys": [
        "jira-core"
    ]
}

{
    "self": "http://www.example.com/jirahttp://www.example.com/jira/rest/api/2/user/charlie",
    "key": "charlie",
    "name": "charlie",
    "emailAddress": "charlie@atlassian.com",
    "displayName": "Charlie of Atlassian"
}

'''

# https://docs.atlassian.com/jira/REST/latest/#api/2/user-addUserToApplication
# POST /rest/api/2/user

def get_project(params):
  api_server = params['api_url']
  api_username = params['api_username']
  api_password = params['api_password']
  auth = (api_username, api_password)
  jira = JIRA( {'server': api_server}, basic_auth=auth)
  key = params['project_key']
  try:
    return jira.project(key)
  except:
    return None

def create_project(params):
  api_server = params['api_url']
  api_username = params['api_username']
  api_password = params['api_password']
  auth = (api_username, api_password)
  jira = JIRA( {'server': api_server}, basic_auth=auth)
  project_key = params['project_key']
  project_name = params['project_name']
  assignee = params['assignee']

  # create project and view
  if not jira.create_project(project_key, name=project_name, assignee=assignee):
    return None
  proj = jira.project(project_key)
  board = jira.create_board("{0} View".format(project_name), project_key, preset='scrum')
  issue = jira.create_issue(
             project=project_key,
             summary="Sample Issue for {0}".format(project_name),
             description="This is just sample",
             issuetype={"name":"Task"}
          )
  return proj

def main():
  m = AnsibleModule(
    argument_spec = dict(
      project_key = dict(required=True),
      project_name = dict(required=True),
      assignee = dict(required=True),
      api_url = dict(required=True),
      api_username = dict(required=True),
      api_password = dict(required=True),
    ))
  p = m.params
  project_key = p['project_key']
  proj = get_project(p)
  if proj is not None:
    m.exit_json( 
      changed=False,
      msg="Project exists: {0}".format(proj),
      rc=0
    )
  proj = create_project(p)
  if proj is not None:
    m.exit_json(
      changed=True,
      msg="Project created: {0}".format(proj),
      rc=0
    )
  m.fail_json(
    changed=False,
    msg="Project creation failed: {0}".format(project_key),
    rc=1
  )


from ansible.module_utils.basic import *
main()

