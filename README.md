# Verteilte-Systeme-Birthday-Abgabe

Die Abgabe ist auch in der folgenden Repository zu finden:
https://github.com/Mehmet1700/Verteilte-Systeme-Birthday-Abgabe

Dies ist die Abgabe für das Projekt "Verteilte Systeme". Es handelt sich um eine REST-API, die mit FastAPI und CouchDB realisiert wurde. Die API ermöglicht es, Daten in einer CouchDB abzurufen.
Die Abgabe ist in drei Teile unterteilt:
1. Auführung lokal
2. Ausführung in einem Docker-Container
3. Ausführung in einem Kubernetes-Cluster


## Lokale Ausführung
### Voraussetzungen
Zuerst wird empfohlen eine virtuelle Umgebung zu erstellen, um die Abhängigkeiten zu installieren. Hierzu kann pipenv verwendet werden. 

Dies kann mit folgendem Befehl i nder Konsole erreicht werden:
```bash
pipenv install
```

Anschließend muss die virtuelle Umgebung aktiviert werden:
```bash
pipenv shell
```

Nun müssen die Requirements installiert werden, welche in der Datei `requirements.txt` aufgelistet sind:
```bash
pip install -r requirements.txt
```

Es ist auch möglich die Abhängigkeiten in der Pipfile zu installieren:
```bash
pipenv install
```

Wir benötigen die CouchDB Datenbank, damit die Anwendung lokal funktionieren kann. 
Die CouchDB Datenbank wurde als Docker Container bereitsgestellt, weshalb wir vorher die CouchDB als Docker Container starten müssen. 
Die CouchDB Datenbank muss als Image gebaut werden. Die Dockerfile befindet sich im Ordner "Couch-DB".
Der Pfade muss zuerst in den Ordner "Couch-DB/ContainerImage" geändert werden.

```bash
cd Couch-DB/ContainerImage
```

Die Dockerfile kann nun gebaut werden:
```bash
docker build -t couchdb .
```

Nun kann der Container gestartet werden:
```bash
docker run -d -p 5984:5984 --name couchdb couchdb
```

Die CouchDB Datenbank läuft nun lokal auf dem Port 5984.
Der FastAPI-Microservice kann nun gestartet werden und mit der CouchDB kommunizieren.

### Ausführung
Der Microservice kann nun gestartet werden. Hierzu muss zuerst in den obersten Ordner des Projekts navigiert werden:

```bash
cd ...
```

```bash
uvicorn src.main:app --host localhost --port 8000 --reload
```

Nun kann die Anwendung unter folgender URL erreicht werden:
```bash
http://localhost:8000
```

Die Dokumentation der API kann unter folgender URL erreicht werden:
```bash
http://localhost:8000/docs
```

Der Health-Check der API kann unter folgender URL erreicht werden:
```bash
http://localhost:8000/health
```
### Erklärung
Die Anwendung hat eine HTML-Oberfläche bekommen, um die Übersichtlichkeit zu gewährleisten.
Es beinhaltet eine Tabelle, welche die abgefragten Daten anzeigt. Desweiteren gibt es ein Formular, um die Daten abzufragen. Sowie einen Button, um den Status der API abzufragen. Diese Funktionalitäten könnten theoretisch auch über einen Curl Befehl abgefragt werden, allerdings ist eine HTML-Oberfläche übersichtlicher und einfacher zu bedienen. Desweiteren wurde eine config.py Datei erstellt, um die Konfigurationen der Anwendung zu speichern. Dadurch wurden wichtige Variablen aus der main.py Datei entfernt und in die config.py Datei verschoben. In dem Code wurde eine If-Abfrage implementiert, welche überprüft, ob die config.py zur Verfügung steht. Der Grund hierfür ist, dass die config.py Datei nicht in einem DockerImage enthalten sein soll, um wichtige Passwörter zu schützen. Deshalb ist die config.py im '.Dockerignore' enthalten, damit sie nicht in das Dockerimage eingefügt wird. Wenn die config.py nicht zur Verfügung steht, wird die Anwendung trotzdem gestartet, aber es werden Environment Variablen aus dem Dockerfile bzw. Docker-Compose-File verwendet. Bei Kubernetes gilt das gleiche, wobei hier die Environment Variablen in einer secret.yml Datei gespeichert werden. Dadurch ist die Gewährleistung der 12-Faktor-Apps möglich. 

## Ausführung in einem Docker-Container
Im nächsten Schritt wird die Anwendung in einem Docker-Container ausgeführt. Hierzu muss der Code in ein Docker-Image gebaut werden. Hierzu gibt es ein Dockerfile, welches sich im Projektordner befindet. Es ist zu empfehlen, dass die vorherige CouchDB gestoppt wird, da die Anwendung eine eigene CouchDB als Docker-Container startet. Außerdem sollte die Anwendung gestoppt werden, da der Port 8000 bereits von der Anwendung verwendet wird.
### Voraussetzungen
Das Dockerfile ist der Bauplan, um das entsprechende Docker-Image zu bauen. Im Dockerfile ist eine Beschreibung des Images enthalten. Darüber hinaus wird die CouchDB als Docker-Container benötigt, um eine Datenbank zur Verfügung zu stellen. Theoretisch ist es möglich, dass beide Images einzeln gebaut werden (Docker build) und dann seperat gestartet werden (Docker run). Allerdings ist es einfacher, wenn beide Images in einem Docker-Compose-File gebaut und gestartet werden. Hierzu wurde ein Docker-Compose-File erstellt, welches sich im Projektordner befindet.
Das Docker-Compose-File beschreibt, wie die Container gestartet werden sollen. Es beschreibt die Abhängigkeiten und die Konfiguration der Container.
### Ausführung
Das bauen des Docker-Images kann mit folgendem Befehl erreicht werden:
```bash
docker build -t my-fastapi-app .
```

Die Docker-Compose-File wird mit folgendem Befehl gestartet, welches den Zusatz --build enthält, um alle enthaltenen Images neu zu bauen und zu starten:
```bash
docker-compose up --build
```


Die FASTAPI Anwendung kann nun unter folgender URL erreicht werden:
```bash
http://localhost:8000
```

Die Datenbank kann unter folgender URL erreicht werden:
```bash
http://localhost:5984
```

Um einen Health Check der Anwendung durchzuführen, kann folgender Link verwendet werden oder die Funktion in der Anwendung ausgeführt werden:
```bash 
http://localhost:8000/health
```

Um einen Health Check der Datenbank durchzuführen, kann folgender Link verwendet werden:
```bash
http://localhost:5984/_up
```

Um in die Admin Console der Datenbank zu gelangen, kann folgender Link verwendet werden:
```bash
http://localhost:5984/_utils/
```

Um die Anwendung zu stoppen, kann folgender Befehl verwendet werden:
```bash
docker-compose down
```

Die Dokumentation der API der FASTAPI kann unter folgender URL erreicht werden:
```bash
http://localhost:8000/docs
```
### Erklärung
Die Docker-Compose-File wurde so konfiguriert, dass die Anwendung und die Datenbank gestartet werden. Die Anwendung ist von der Datenbank abhängig, weshalb die Anwendung erst gestartet wird, wenn die Datenbank gestartet wurde. Die Konfigurationen der Environment wurde in einer .env-Datei gespeichert. Die .env-Datei wird von der Docker-Compose-File gelesen und die Variablen werden in den Containern gesetzt. Wir benötigen diese, da wird die config.py nicht in das Image einlesen.  


## Ausführung in einem Kubernetes-Cluster
Im letzten Schritt wird die Anwendung in einem Kubernetes-Cluster ausgeführt.
### Voraussetzungen
Zuerst muss ein Kubernetes-Cluster erstellt werden. Hierzu wird DockerDesktop verwendet, aber auch minikube wäre möglich. In dem deployment Ordner befinden sich die Konfigurationen für das Deployment, Service, ConfigMap und Secret. Diese werden benötigt, um das Cluster zu konfigurieren.
### Ausführung
Es gibt die Möglichkeit, dass alle Konfigurationen mit einem Befehl ausgeführt werden. Hierzu kann folgender Befehlt genutzt werden, womit alle in dem deployment Ordner enthaltenen Konfigurationen ausgeführt werden:
```bash
kubectl apply -f deployment/
```

Es ist auch möglich, dass die Konfigurationen einzeln ausgeführt werden. Hierzu kann folgender Befehl genutzt werden:
```bash
kubectl apply -f deployment/fastapi-k8-deployment.yml
kubectl apply -f deployment/fastapi-k8-service.yml
kubectl apply -f deployment/fastapi-k8-configmap.yml
kubectl apply -f deployment/fastapi-k8-secret.yml
kubectl apply -f deployment/couchdb-k8-deployment.yml
kubectl apply -f deployment/couchdb-k8-service.yml
```

Es kann vorkommen, dass bei anderen Kubernetes Clustern wie Kind oder minikube das laden der Images aus Docker erfolgen muss.
Dies ist z.B. der Fall, wenn Fehler wie "ImagePullBackOff" oder "ErrImagePull" auftreten. 
Hierzu kann folgender Befehl genutzt werden:
```bash
eval $(minikube docker-env)
```
Im Anschluss kann das Image überprüft werden mit dem Befehl:
```bash
docker images
```

Falls es immernoch nicht auftaucht, können die einzelnen Images mit folgendem Befehl geladen werden:
```bash
docker load -i <image.tar>
```
Für Minikube kann folgender Befehl genutzt werden:
```bash
minikube image load <image>
```

Für unsere Images sieht das wie folgt aus:
```bash
docker load -i fastapi.tar
docker load -i couchdb.tar
```

Im Anschluss sollte wieder überprüft werden, ob das laden funktioniert hat mit dem vorherigen Befehl docker images.


Das Deployment kann nun unter folgender URL erreicht werden:
```bash
http://localhost:30000
```

Die Dokumentation der API der FASTAPI kann unter folgender URL erreicht werden:
```bash
http://localhost:30000/docs
```

Der Health-Check der API kann unter folgender URL erreicht werden:
```bash
http://localhost:30000/health
```

Das stoppen der Deployments, Services, ConfigMaps und Secrets kann mit folgendem Befehl erreicht werden:
```bash
kubectl delete deployment --all
kubectl delete service --all
kubectl delete configmap --all
kubectl delete secret --all
```

### Erklärung
Die Konfigurationen wurden in den entsprechenden Dateien gespeichert. Die Environment Variablen wurden in einer secret.yml Datei gespeichert. Die secret.yml Datei wurde in das Kubernetes-Cluster geladen. Die Anwendung wurde in einem Deployment gestartet und der Service wurde als Nodeport konfiguriert. Die CouchDB wurde ebenfalls in einem Deployment gestartet und der Service wurde als Nodeport konfiguriert. Die ConfigMap wurde für die Konfiguration der Anwendung verwendet. Die einzelnen Konfigurationen wurden mit Kommentaren versehen, um die Funktionalität zu erklären.