#!/usr/bin/env python

'''
TODO
- Add role access
- Add maven repo type
- Yum repo: with proxy and sync rules

'''
DOCUMENTATION = '''
---
module: artifactory_repo
short_description: CRUD operation for artifactory repo through Artifactory REST api
description:
     - Create, Read, Write, Update generic or yum repo from the artifactory
     - https://www.jfrog.com/confluence/display/RTF/Artifactory+REST+API
version_added: "0.1.0"
options:
  state:
    description:
      - "ensure if repo exists"
    required: yes
    choices: ["present", "absent"]
    default: "present"
  api_url:
    description:
      - "Artifactory API url"
    required: yes
  api_username:
    description:
      - "Artifactory API username"
    required: yes
  api_password:
    description:
      - "Artifactory API password"
    required: yes
  repo_key:
    description:
      - "Repo Key"
    required: yes
  rclass:
    description:
      - "Type of repo (local|remote)"
    required: no
    choices: ["local", "remote"]
  package_type:
    description:
      - "Packaging type (generic|yum|maven)"
    required: no
    choices: ["generic", "yum", "maven"]
    default: "generic"
  remote_url:
    description:
      - "Remote URL - for remote repo only."
    required: no
    default: null
  description:
    description:
      - "Description of the repo"
    required: no
    default: ""
  notes:
    description:
      - "Usage note for repo"
    required: no
    default: ""

notes: Tested with Artifactory Pro only at this time
requirements: Ansible 1.8.2 or higher
author: Hoi_Tsang@mckinsey.com
'''
EXAMPLES = '''

# create yum repo
artifactory_repo:
  state=present
  api_url=http://localhost:8081/artifactory/api
  api_username=admin
  api_password=password
  repo_key=jenkins-stable
  package_type=yum
  remote_url=http://pkg.jenkins-ci.org/redhat-stable
  description="Local yum repo for Jenkins stable releases"
  notes="Read-only"

# delete yum repo
artifactory_repo:
  state=absent
  api_url=http://localhost:8081/artifactory/api
  api_username=admin
  api_password=password
  repo_key=jenkins-stable
'''

import json
import requests


def do_http_request(request_type, payload, module_params):
  p = module_params
  a = (p['api_username'], p['api_password'])
  h = {'Content-type': 'application/json'}
  u = "{0}/security/permissions/{1}".format(p['api_url'], "{0}_readwrite".format(p['repo_key']))
  if 'get' == request_type:
    return requests.get(url=u, headers=h, auth=a, data=payload)
  if 'post' == request_type:
    return requests.post(url=u, headers=h, auth=a, data=payload)
  if 'put' == request_type:
    return requests.put(url=u, headers=h, auth=a, data=payload)
  if 'delete' == request_type:
    return requests.delete(url=u, headers=h, auth=a, data=payload)
  return None

def security_group_exists(ansible_module):
  p = ansible_module.params
  resp = do_http_request('get', None, p)
  if resp.status_code != 200:
    return False
  return True

def create_security_group(ansible_module):
  p = ansible_module.params
  return do_http_request('put', get_security_group_payload(p), p)

def get_security_group_payload(params):
  p = params
  d = { "name": "{0}_readwrite".format(p['repo_key']),
        "includesPattern": "**",
        "exciudesPattern": "",
        "repositories": [p['repo_key']],
        "principals": { "users": {} }
      }
  for u in p["repo_users"].split(","):
    d["principals"]["users"][u.strip()] = p["repo_permissions"].split(",")
  return json.dumps(d)

def main():
  m = AnsibleModule(
    argument_spec     = dict(
      api_url = dict(required=True),
      api_username = dict(required=True),
      api_password = dict(required=True),
      repo_key = dict(required=True),
      repo_users = dict(required=True),
      repo_permissions = dict(required=True)
    ))
  p = m.params
  sec_group_name = "{0}_readwrite".format(p['repo_key'])
  if security_group_exists(m):
     m.exit_json(changed=False, status="Security group exists: {0}".format(sec_group_name))
  r = create_security_group(m)
  if r.status_code not in (200, 201):
     m.fail_json(msg="Failed to create security group: {0}, errors: {1}".format(sec_group_name, r.content))
  m.exit_json(changed=True, status="Security group created: {0}".format(sec_group_name))


from ansible.module_utils.basic import *
main()
