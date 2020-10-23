void setBuildStatus(String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/karx1/simplecdn"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "Jenkins CI"],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}

node {
	def app
	stage('Clone repository') {
		checkout scm
	}
	stage('Set pending status') {
	    setBuildStatus("Build pending", "PENDING");
	}
	try {
	    stage('build') {
		    app = docker.build("karx/simplecdn")
	    }
		stage("Test Image") {
			app.inside() {
				sh "cd /app"
				sh "rm -rf data"
				sh "DATA_DIR=/app/data DEBUG=true python -m unittest discover --verbose"
			}
		}
	    stage('Push image') {
		    def version = readFile("version.txt")
		    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
		  	    app.push("latest")
                            app.push(version)
		    }
	    }
	} catch (e) {
	    setBuildStatus("Build failed", "FAILURE");
	    withCredentials([string(credentialsId: 'karx-discord-webhook', variable: 'DISCORD')]) {
		    discordSend webhookURL: DISCORD, title: "Jenkins Pipeline Build", link: env.BUILD_URL, result: currentBuild.currentResult, footer: "SimpleCDN", description: "Build FAILURE"
		}
	    throw e
	} finally {
	    setBuildStatus("Build succeeded", "SUCCESS");
	    withCredentials([string(credentialsId: 'karx-discord-webhook', variable: 'DISCORD')]) {
		    discordSend webhookURL: DISCORD, title: "Jenkins Pipeline Build", link: env.BUILD_URL, result: currentBuild.currentResult, footer: "SimpleCDN", description: "Build SUCCESS"
		}
	}
}
