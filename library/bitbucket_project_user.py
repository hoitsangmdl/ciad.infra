#!/usr/bin/env python
# https://developer.atlassian.com/static/rest/bitbucket-server/4.2.0/bitbucket-rest.html

import json
import requests
from bitbucket import bitbucket
from pprint import pprint


def project_user_exists(params):
  api_url = "{0}/rest/api/1.0/projects/{1}/repos/{2}".format(
              params["api_url"],
              params["project_key"],
              params["repo_slug"]
             )
  api_auth = (params["api_username"], params["api_password"])
  headers = {"Content-type": "application/json"}
  r = requests.get(api_url, auth=api_auth, headers=headers)
  if r.status_code != 200:
    return r, False
  return r, True
    
def create_project_user(params):
  api_url = "{0}/rest/api/1.0/projects/{1}/permissions/users".format(
              params["api_url"],
              params["project_key"]
             )
  api_url = "{0}?name={1}&permission={2}".format(api_url, params['username'], params['permission'])
  api_auth = (params["api_username"], params["api_password"]) 
  headers = {"Content-type": "application/json"}
  return requests.put(api_url, auth=api_auth, headers=headers)

def main():
  m = AnsibleModule(
    argument_spec = dict(
      project_key = dict(required=True),
      username = dict(required=True),
      permission = dict(required=True),
      api_url = dict(required=True),
      api_username = dict(required=True),
      api_password = dict(required=True),
    ))
  p = m.params
  #r, exists = project_user_exists(p)
  #if 200 == r.status_code and exists:
  #  m.exit_json(
  #    changed=False,
  #    stdout=r.content,
  #    status="Repo user exists: {0}/{1}".format(p['project_key'],p['username']),
  #    rc=0
  #  )

  r = create_project_user(p)
  if r.status_code in (200, 204):
    m.exit_json(
      changed=True,
      stdout=r.content,
      status="Project user created: {0}/{1}".format(p['project_key'],p['username']),
      rc=0
    )

  msg="Repo user creation failed: {0}/{1}".format(
        p['project_key'],p['username']
       )
  err="Status_code: {0}, errors: {1}".format(r.status_code, r.content)
  m.fail_json(
    msg=msg,
    stderr=err,
    rc=1
  )


from ansible.module_utils.basic import *
main()
