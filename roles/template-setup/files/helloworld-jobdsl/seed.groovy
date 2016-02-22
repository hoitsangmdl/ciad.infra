def gitUrl = 'ssh://git@{{scm_host}}:{{scm_port}}/{{project_key}}/{{repo_name|lower}}.git'
def gitDeployUrl = 'ssh://git@{{scm_host}}:{{scm_port}}/{{project_key}}/{{repo_name|lower}}-deploy.git'

job('{{project_key}}-{{repo_name|lower}}-snapshot-build') {
    scm {
        git(gitUrl) { node -> // is hudson.plugins.git.GitSCM
            node / gitConfigName('jenkins')
            node / gitConfigEmail('jenkins@localhost')
        }
    }
    label('master')
    triggers {
        scm('*/15 * * * *')
    }
    steps {
      maven {
        mavenInstallation('3.3.9')
        goals('-e clean test package deploy')
      }
    }
}

freeStyleJob('{{project_key}}-{{repo_name|lower}}-snapshot-deploy') {
    scm {
        git(gitDeployUrl) { node -> // is hudson.plugins.git.GitSCM
            node / gitConfigName('jenkins')
            node / gitConfigEmail('jenkins@localhost')
        }
    }
    label('master')
    steps {
      shell('./deploy.sh')
    }
}


job('{{project_key}}-{{repo_name|lower}}-release') {
    scm {
        git(gitUrl) { node -> // is hudson.plugins.git.GitSCM
            node / gitConfigName('jenkins')
            node / gitConfigEmail('jenkins@localhost')
            node / wipeOutWorkspace(true)
            node / createTag(true)
            node / localBranch("master")
        }
    }
    label('master')
    steps {
      maven {
        mavenInstallation('3.3.9')
        goals('-X release:clean release:prepare release:perform')
      }
    }
}


listView('{{project_key}}') {
    description('All jobs for {{project_key}}')
    filterBuildQueue()
    filterExecutors()
    jobs {
        regex(/{{project_key}}-.+/)
    }
    columns {
        status()
        weather()
        name()
        lastSuccess()
        lastFailure()
        lastDuration()
        buildButton()
    }
}
