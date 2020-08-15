node {
	def app
	stage('Clone repository') {
		checkout scm
	}
	stage('build') {
		app = docker.build("karx1/simplecdn")
	}
	stage('Push image') {
		docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
			app.push("latest")
		}
	}
}
