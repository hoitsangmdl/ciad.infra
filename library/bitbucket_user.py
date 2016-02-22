#!/usr/bin/env python
# https://developer.atlassian.com/static/rest/bitbucket-server/4.2.0/bitbucket-rest.html

'''

  bitbucket_user:
    state: present
    name: ProjectOne_admin
    password: .ProjectOne_admin
    display_name: ProjectOne Admin
    email_address: hoi.h.tsang@gmail.com
    add_to_default_group: true

  /rest/api/1.0/projects/{projectKey}/permissions/users

  bitbucket_project:
    state: present
    namespace: ProjectOne
    key: ProjectOne
    name: ProjectOne
    api_host: ...
    api_username: admin
    api_password: password
    admin_user: ProjectOne_admin

  /rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/permissions/users

  bitbucket_repo:
    state: present
    project_key: ProjectOne
    name: ProjectOne webapp
    scmId: git
    forkable: true
    api_host: ...
    api_username: admin
    api_password: password
    admin_user: ProjectOne_admin




{
    "name": "My repo",
    "scmId": "git",
    "forkable": true
}


'''

import json
import requests
from bitbucket import bitbucket
from pprint import pprint


def user_exists(params):
  payload = {"filter": params["username"]}
  api_url = "{0}/rest/api/1.0/admin/users".format( params['api_url'])
  api_auth = (params["api_username"], params["api_password"])
  headers = {"Content-type": "application/json"}
  r = requests.get(api_url, auth=api_auth, params=payload, headers=headers)
  if r.status_code != 200:
    return r, False
  c = json.loads(r.content)
  for p in c['values']:
    if p['name'] == params['username']:
      return r, True
  return r, False
    
def create_user(params):
  payload = {"name": params["username"],
             "password": ".{0}".format(params["username"]),
             "emailAddress": params["email_address"],
             "displayName": params["display_name"]}
  api_url = "{0}/rest/api/1.0/admin/users".format( params['api_url'])
  api_auth = (params["api_username"], params["api_password"])
  headers = {"Content-type": "application/json"}
  return requests.post(api_url, auth=api_auth, params=payload, headers=headers)

def main():
  m = AnsibleModule(
    argument_spec = dict(
      username = dict(required=True),
      password = dict(required=True),
      display_name = dict(required=True),
      email_address = dict(required=True),
      api_url = dict(required=True),
      api_username = dict(required=True),
      api_password = dict(required=True),
    ))
  p = m.params
  r, exists = user_exists(p)
  if 200 == r.status_code and exists:
    m.exit_json(
      changed=False,
      stdout=r.content,
      status="User exists: {0}".format(p['username']),
      rc=0
    )

  r = create_user(p)
  if r.status_code in (200, 204):
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
