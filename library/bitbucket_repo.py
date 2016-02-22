#!/usr/bin/env python
# https://developer.atlassian.com/static/rest/bitbucket-server/4.2.0/bitbucket-rest.html

import json
import requests
from bitbucket import bitbucket
from pprint import pprint


def repo_exists(params):
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
    
def create_repo(params):
  api_url = "{0}/rest/api/1.0/projects/{1}/repos".format(
              params["api_url"],
              params["project_key"]
             )
  payload = {'name': params['repo_slug'], 
             'scmId': 'git',
             'forkable': True}
  payload = json.dumps(payload)
  api_auth = (params["api_username"], params["api_password"]) 
  headers = {"Content-type": "application/json"}
  return requests.post(api_url, data=payload, auth=api_auth, headers=headers)

def main():
  m = AnsibleModule(
    argument_spec = dict(
      project_key = dict(required=True),
      repo_slug = dict(required=True),
      api_url = dict(required=True),
      api_username = dict(required=True),
      api_password = dict(required=True),
    ))
  p = m.params
  r, exists = repo_exists(p)
  if 200 == r.status_code and exists:
    m.exit_json(
      changed=False,
      stdout="fooo {0}".format(r.content),
      status="Repo exists: {0}/{1}".format(p['project_key'],p['repo_slug']),
      rc=0
    )

  r = create_repo(p)
  if r.status_code in (200, 201):
    m.exit_json(
      changed=True,
      stdout=r.content,
      status="Repo created: {0}".format(p['repo_slug']),
      rc=0
    )

  msg="Repo creation failed: {0}/{1}".format(p['project_key'],p['repo_slug'])
  err="Status_code: {0}, errors: {1}".format(r.status_code, r.content)
  m.fail_json(
    msg=msg,
    stderr=err,
    rc=1
  )


from ansible.module_utils.basic import *
main()
