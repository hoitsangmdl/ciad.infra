#!/usr/bin/env python

DOCUMENTATION = '''
---
module: artifactory_fetch
short_description: check and download external file, and then cache copy to artifactory generic repo
description:
     - used for generic fetch and cache, non-maven, non-yum.
     - follow company/product/product-version/product-version.ext format
version_added: "0.1.0"
options:
  repo_item_url:
    description: 
      - "repository location of the item"
  fetch_cmd:
    desccription: 
      - "item url to be fetch"
    required: yes
  local_path:
    description:
      - "local copy"
  repo_username:
    description:
      - "Artifactory API username"
    required: yes
  repo_password:
    description:
      - "Artifactory API password"
    required: yes
    
notes: Tested with Artifactory Pro only at this time
requirements: Ansible 1.8.2 or higher
author: Hoi_Tsang@mckinsey.com
'''
EXAMPLES = '''

# create yum repo
artifactory_fetch:
  repo_item_url: http://localhost:8081/artifactory/local-generic/oracle/jdk/8u65-b17/jdk-8u65.tar.gz
  fetch_cmd: com/otn-pub/java/jdk/{{jdk_version}}/{{jdk_archive}} 
  local_path: /tmp/jdk-8u65.tar.gz
  repo_username: admin
  repo_password: password
  refresh: True
'''
import json
import shlex
from subprocess import Popen, PIPE

import requests


def file_exists(params):
  url = params['repo_item_url']
  r = requests.get(url, stream=True)
  return r.status_code == 200

def fetch_file(params):
  fetch_cmd = shlex.split(''.join(params['fetch_cmd']).replace('\n', ''))
  p = Popen(fetch_cmd, stdout=PIPE, stderr=PIPE)
  stdout, stderr = p.communicate()
  return p.returncode, stdout, stderr

def remove_repo_file(params):
  url = params['repo_item_url']
  auth = (params['repo_username'], params['repo_password'])
  r = requests.delete(url=url, auth=auth)
  return r.status_code not in (200, 201)

def upload_new_file_to_repo(params):
  local_path = params['local_path']
  url = params['repo_item_url']
  auth = (params['repo_username'], params['repo_password'])
  d = open(local_path, 'rb')
  r = requests.put(url=url, auth=auth, data=d)
  return r.status_code in (200, 201)


def main():
  m = AnsibleModule(
    argument_spec = dict(
      repo_item_url = dict(required=True),
      fetch_cmd = dict(required=True),
      local_path = dict(required=True),
      repo_username = dict(required=True),
      repo_password = dict(required=True),
      refresh = dict(required=False)
    ))
  p = m.params

  repo_item_url = p['repo_item_url'] 
  local_path = p['local_path']
  fetch_cmd = shlex.split(''.join(p['fetch_cmd']).replace('\n', '').strip())
  refresh = p['refresh']
  
  file_exists_in_repo = file_exists(p)
  if file_exists_in_repo and not refresh:
    m.exit_json(changed=False, status="File exists in repo: {0}".format(repo_item_url))

  # refresh file
  fetch_cmd_return_code, fetch_cmd_stdout, fetch_cmd_stderr = fetch_file(p)
  if fetch_cmd_return_code != 0:
    m.fail_json(msg="File fetch command failed: {0}, output: {1}, error: {2}, return_code: {3}"
	.format(fetch_cmd, fetch_cmd_stdout, fetch_cmd_stderr, fetch_cmd_return_code))
  if not os.path.exists(local_path):
    m.fail_json(msg="File fetched not found: {0}".format(local_path))

  # remove old file
  if refresh and file_exists_in_repo:
    if not remove_repo_file(p):
      m.fail_json(msg="Failed to remove item from repo: {0}".format(repo_item_url))

  # upload new download to repo
  if not upload_new_file_to_repo(p):
    m.fail_json(msg="Failed to upload item: {0}, error: {1}".format(repo_item_url, r.content))

  # clean up
  os.remove(local_path)

  m.exit_json(changed=True, status="local item: {0} uploaded to {1}".format(local_path, repo_item_url))
 
  


from ansible.module_utils.basic import *
main()

