#!/usr/bin/env python
# setup project user
# setup project repo seed job
# setup project view
# https://github.com/jenkinsci/job-dsl-plugin

job_config = '''<?xml version="1.0" encoding="UTF-8"?>
<project>
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@2.4.1">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>ssh://git@%(scm_host)s:%(scm_port)s/%(project_key)s/%(repo_name)s.git</url>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>*/master</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <javaposse.jobdsl.plugin.ExecuteDslScripts plugin="job-dsl@1.42">
      <targets>seed.groovy</targets>
      <usingScriptText>false</usingScriptText>
      <ignoreExisting>false</ignoreExisting>
      <removedJobAction>IGNORE</removedJobAction>
      <removedViewAction>IGNORE</removedViewAction>
      <lookupStrategy>JENKINS_ROOT</lookupStrategy>
      <additionalClasspath></additionalClasspath>
    </javaposse.jobdsl.plugin.ExecuteDslScripts>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>'''

import json
import requests

from jenkinsapi.jenkins import Jenkins

def main():
  m = AnsibleModule(
    argument_spec = dict(
      project_key = dict(required=True),
      repo_name = dict(required=True),
      scm_host = dict(required=True),
      scm_port = dict(required=True),
      api_url = dict(required=True),
      api_username = dict(required=True),
      api_password = dict(required=True),
    ))
  p = m.params
  p['repo_name'] = p['repo_name'].lower()
  job_name = "{0}-{1}".format(p['project_key'], p["repo_name"])
  view_name = p['project_key']

  jenkins = Jenkins(p['api_url'],
                    p['api_username'],
                    p['api_password'])

  if jenkins.has_job(job_name):
    m.exit_json(changed=False, status="Job already exists: {0}".format(job_name))

  cfg = job_config % p
  job = jenkins.create_job(job_name, cfg)
  if job is None:
    m.fail_json(msg="Failed to create job: {0}".format(cfg))

  # create view
#  if view_name not in jenkins.views:
#    view = jenkins.views.create(view_name)
#    view.add(job_name)

  jenkins.build_job(job_name)
  m.exit_json(changed=True, status="DSL Job created: {0}".format(job_name))


from ansible.module_utils.basic import *
main()
