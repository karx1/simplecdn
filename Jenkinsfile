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
	    stage('Push image') {
		    def version = readFile("version.txt")
		    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
		  	    app.push("latest")
                            app.push(version)
		    }
	    }
	} catch (e) {
	    setBuildStatus("Build failed", "FAILURE");

	    throw e
	} finally {
	    setBuildStatus("Build succeeded", "SUCCESS");
	}
}
