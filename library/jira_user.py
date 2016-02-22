#!/usr/bin/env python
import json
import requests

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

def user_exists(params):
  app_keys = [f.strip() for f in params['app_keys'].split(',')]
  payload = {"username": params["username"]}
  api_url = "{0}/rest/api/2/user".format( params['api_url'])
  api_auth = (params["api_username"], params["api_password"])
  headers = {"Content-type": "application/json"}
  return requests.get(api_url, auth=api_auth, params=payload, headers=headers) 

def create_user(params):
  app_keys = [f.strip() for f in params['app_keys'].split(',')]
  payload = {"name": params["username"],
             "password": ".{0}".format(params["username"]),
             "emailAddress": params["email_address"],
             "displayName": params["display_name"],
             "applicationKeys": app_keys}
  api_url = "{0}/rest/api/2/user".format( params['api_url'])
  api_auth = (params["api_username"], params["api_password"])
  headers = {"Content-type": "application/json"}
  return requests.post(api_url, auth=api_auth, data=json.dumps(payload), headers=headers)


def main():
  m = AnsibleModule(
    argument_spec = dict(
      username = dict(required=True),
      password = dict(required=True),
      display_name = dict(required=True),
      email_address = dict(required=True),
      app_keys = dict(required=True),
      api_url = dict(required=True),
      api_username = dict(required=True),
      api_password = dict(required=True),
    ))
  p = m.params

  r = user_exists(p)
  if 200 == r.status_code:
    m.exit_json(
      changed=False,
      stdout=r.content,
      status="User exists: {0}".format(p['username']),
      rc=0
    )

  r = create_user(p)
  if r.status_code in (200, 201):
    m.exit_json(
      changed=True,
      stdout=r.content,
      status="User created: {0}".format(p['username']),
      rc=0
    )

  msg="User creation failed: {0}".format(p['username'])
  err="status_code: {0}, errors: {1}".format(r.status_code, r.content)
  m.fail_json(
    msg=msg,
    stderr=err,
    rc=1
  )
  

from ansible.module_utils.basic import *
main()

