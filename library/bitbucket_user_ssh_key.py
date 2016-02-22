#!/usr/bin/env python
# https://developer.atlassian.com/static/rest/bitbucket-server/4.2.0/bitbucket-rest.html

import json
import requests
from bitbucket import bitbucket
from pprint import pprint


def user_ssh_key_exists(params):
  api_url = "{0}/rest/ssh/1.0/keys?user={1}".format(
              params["api_url"],
              params["username"]
             )
  api_auth = (params["api_username"], params["api_password"])
  headers = {"Content-type": "application/json"}
  r = requests.get(api_url, auth=api_auth, headers=headers)
  if r.status_code != 200:
    return r, False
  j = json.loads(r.content)
  for key in j['values']:
    if key['text'] == params['ssh_key_text']:
      return r, True
  return r, False

def create_user_ssh_key(params):
  api_url = "{0}/rest/ssh/1.0/keys?user={1}".format(
              params["api_url"],
              params["username"]
             )
  payload = { 'text': params['ssh_key_text'] }
  payload = json.dumps(payload)
  api_auth = (params["api_username"], params["api_password"])
  headers = {"Content-type": "application/json"}
  return requests.post(api_url, auth=api_auth, headers=headers, data=payload)

def main():
  m = AnsibleModule(
    argument_spec = dict(
      username = dict(required=True),
      ssh_key_text = dict(required=True),
      api_url = dict(required=True),
      api_username = dict(required=True),
      api_password = dict(required=True),
    ))
  p = m.params
  r, exists = user_ssh_key_exists(p)
  if exists:
    m.exit_json(
      changed=False,
      stdout=r.content,
      status="User key already exists: {0}".format(p['username']),
      rc=0
    )
  r = create_user_ssh_key(p)
  if r.status_code in (200, 201):
    m.exit_json(
      changed=True,
      stdout=r.content,
      status="User key created: {0}".format(p['username']),
      rc=0
    )

  msg = "User key creation failed: {0}/{1}".format(p['username'], p['ssh_key_text'])
  err = "Status_code: {0}, errors: {1}".format(r.status_code, r.content)
  m.fail_json(
    msg=msg,
    stderr=err,
    rc=1
  )


from ansible.module_utils.basic import *
main()
