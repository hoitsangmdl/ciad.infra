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


def project_exists(params):
  payload = {"name": params["key"]}
  api_url = "{0}/rest/api/1.0/projects/{1}".format(
              params['api_url'], params['key']
            )
  api_auth = (params["api_username"], params["api_password"])
  headers = {"Content-type": "application/json"}
  r = requests.get(api_url, auth=api_auth, headers=headers)
  if r.status_code != 200:
    return r, False
  return r, True
    
def create_project(params):
  payload = {"namespace": params["namespace"],
             "key": params["key"],
             "name": params["name"]}
  payload = json.dumps(payload)
  api_url = "{0}/rest/api/1.0/projects".format( params['api_url'])
  api_auth = (params["api_username"], params["api_password"])
  headers = {"Content-type": "application/json"}
  return requests.post(api_url, auth=api_auth, data=payload, headers=headers)

def public_accessible(params):
  payload = json.dumps({'public': True})
  api_url = "{0}/rest/api/latest/projects/{1}".format(
              params['api_url'], params['key'])
  api_auth = (params["api_username"], params["api_password"])
  headers = {"Content-type": "application/json"}
  return requests.put(api_url, auth=api_auth, data=payload, headers=headers)

def main():
  m = AnsibleModule(
    argument_spec = dict(
      namespace = dict(required=True),
      key = dict(required=True),
      name = dict(required=True),
      api_url = dict(required=True),
      api_username = dict(required=True),
      api_password = dict(required=True),
      public_accessible = dict(required=False, default=False)
    ))
  p = m.params
  r, exists = project_exists(p)
  if 200 == r.status_code and exists:
    m.exit_json(
      changed=False,
      stdout=r.content,
      status="Project exists: {0}".format(p['namespace']),
      rc=0
    )

  r = create_project(p)
  if r.status_code in (200, 201):
    if p['public_accessible']:
      r = public_accessible(p)
      if r.status_code not in (200, 201):
        m.fail_json(msg='Project created but failed to setup public accessble permission', rc=1)
    m.exit_json(
      changed=True,
      stdout=r.content,
      status="Project created: {0}".format(p['namespace']),
      rc=0
    )

  msg="Project creation failed: {0}".format(p['namespace'])
  err="Status_code: {0}, errors: {1}".format(r.status_code, r.content)
  m.fail_json(
    msg=msg,
    stderr=err,
    rc=1
  )


from ansible.module_utils.basic import *
main()
