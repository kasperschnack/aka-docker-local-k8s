# Docker Workshop: Fra container til lokal Kubernetes

Velkommen til en lokal variant af workshoppen. Ideen er den samme som i `aka-docker-azure`: du starter med Docker, bygger dine egne images og kører flere services sammen. Forskellen er, at anden halvdel ikke handler om Azure men om at køre workloads i et lokalt Kubernetes-cluster.

Målet er ikke at bygge en perfekt platform. Målet er at gøre Kubernetes mindre abstrakt.

Du kommer til at:
- Forstå hvad containere er og hvorfor de er nyttige
- Bygge dine egne Docker-images
- Køre en app og en database sammen lokalt
- Oprette et lokalt cluster med `kind`
- Deploye din app med `Deployment` og `Service`
- Bruge `kubectl` til at se pods, logs og events

## Laeringsmaal

### Du vil laere om:

- Docker fundamentals
  - Hvad er en container?
  - Forskellen paa containere og virtuelle maskiner
  - Images, containers og lag

- Praktisk Docker
  - Installation og opsaetning
  - Docker CLI
  - Volumes og netvaerk

- Docker Compose
  - Flere services i samme setup
  - En webapp og en database lokalt

- Lokal Kubernetes
  - Hvad et cluster egentlig er
  - `kind`, `kubectl` og container runtime
  - `Pod`, `Deployment`, `Service` og `Namespace`
  - Port-forwarding, logs og simpel fejlfinding

- Hands-on
  - Byg en Flask-app
  - Kør den med Docker
  - Deploy den i lokal Kubernetes

## Sektion 1: Containere

### Trin 1: Kom i gang med Docker

Docker Desktop er den nemmeste vej paa macOS og Windows. Paa Linux kan du installere Docker Engine direkte.

Ubuntu eksempel:

```bash
sudo apt update
sudo apt install docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

Log ud og ind igen hvis du har koert `usermod`.

### Trin 2: Test at Docker virker

```bash
docker run hello-world
```

Hvis du ser `Hello from Docker!`, er du klar.

### Udforsk Docker CLI

```bash
docker pull nginx
docker images
docker run -d -p 8080:80 nginx
docker ps
docker stop <container-id>
docker rm <container-id>
```

Besøg `http://localhost:8080`.

## Byg din egen container

Der ligger et lille eksempel i [examples/flask-demo](/home/kasc/projects/k8s-session/aka-docker-local-k8s/examples/flask-demo).

Byg imaget:

```bash
cd examples/flask-demo
docker build -t flask-demo:local .
```

Kør det:

```bash
docker run --rm -p 5000:5000 flask-demo:local
```

Besøg `http://localhost:5000`.

### Hvad er der i Dockerfile'en?

- Vi starter fra `python:3.11-slim`
- Vi kopierer `requirements.txt` foerst for bedre caching
- Vi installerer Flask
- Vi kopierer resten af appen ind bagefter

## Volumes og bind mounts

Containere er som udgangspunkt stateless. Hvis du vil gemme data mellem koersler, skal du gemme det uden for containerens eget filsystem.

Volume eksempel:

```bash
docker run -v minvolume:/data busybox sh -c "echo 'Hej fra mit volume' > /data/hilsen.txt"
docker run -v minvolume:/data busybox cat /data/hilsen.txt
```

Bind mount eksempel:

```bash
docker run -v $(pwd)/output:/data busybox sh -c "echo 'Hej fra bind mount' > /data/hilsen.txt"
cat output/hilsen.txt
```

## Docker Compose med web og database

Der ligger et eksempel i [examples/flask-postgres](/home/kasc/projects/k8s-session/aka-docker-local-k8s/examples/flask-postgres).

Koer det lokalt:

```bash
cd examples/flask-postgres
docker compose up --build
```

Besøg `http://localhost:5000`.

Det setup er vigtigt, fordi det ligner noget, du senere vil splitte op i Kubernetes-ressourcer.

## Sektion 2: Lokal Kubernetes

Nu skifter vi perspektiv. I stedet for at sende vores image til en cloud-provider bruger vi et lokalt cluster, saa du kan laere de samme grundbegreber uden at betale for noget eller rydde op i cloud-ressourcer bagefter.

## Hvorfor `kind`?

`kind` betyder Kubernetes IN Docker. Det er et let setup til lokal laering:

- Hurtigt at oprette og slette
- Kører paa din egen maskine
- Godt til at laere `kubectl` og manifests
- Ingen Azure-konto eller registry er noedvendig

Hvis maalet er at forstaa begreberne, er `kind` et bedre første skridt end at hoppe direkte i managed Kubernetes.

## Trin 3: Installer vaerktoejer

Du skal bruge:

- Docker
- `kubectl`
- `kind`

`kubectl`:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

`kind`:

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

Tjek versioner:

```bash
docker --version
kubectl version --client
kind version
```

## Trin 4: Opret et cluster

```bash
kind create cluster --name workshop
```

Tjek at clusteret findes:

```bash
kind get clusters
kubectl cluster-info
kubectl get nodes
```

## Trin 5: Byg et image og load det ind i clusteret

Vi bruger samme Flask-app som foer.

```bash
cd examples/flask-demo
docker build -t flask-demo:local .
kind load docker-image flask-demo:local --name workshop
```

`kind` kan ikke automatisk se alle images fra din lokale Docker daemon som et normalt registry ville kunne. Derfor loader vi imaget direkte ind i clusteret.

## Trin 6: Deploy appen i Kubernetes

Der ligger manifests i [examples/flask-demo/k8s](/home/kasc/projects/k8s-session/aka-docker-local-k8s/examples/flask-demo/k8s).

Anvend dem:

```bash
kubectl apply -f examples/flask-demo/k8s
```

Se hvad der bliver oprettet:

```bash
kubectl get namespaces
kubectl get deployments -n workshop
kubectl get pods -n workshop
kubectl get services -n workshop
```

## Trin 7: Gør appen tilgaengelig

I et lokalt cluster er `port-forward` den enkleste vej:

```bash
kubectl port-forward -n workshop service/flask-demo 5000:5000
```

Besøg `http://localhost:5000`.

## Hvad er forskellen paa de vigtigste ressourcer?

- `Pod`: den konkrete instans der koerer dine containere
- `Deployment`: beskriver hvordan pods skal oprettes og holdes i live
- `Service`: giver en stabil netvaerksadresse til en eller flere pods
- `Namespace`: en logisk opdeling i clusteret

En god mental model er:

- Docker koerer containere
- Compose koerer flere containere sammen
- Kubernetes holder workloads koerende og giver dig en deklarativ model

## Trin 8: Fejlfinding med `kubectl`

De vigtigste kommandoer i starten er:

```bash
kubectl get pods -A
kubectl describe pod <pod-navn> -n workshop
kubectl logs deployment/flask-demo -n workshop
kubectl get events -n workshop --sort-by=.lastTimestamp
```

Hvis en pod ikke starter, er `describe` og `logs` som regel det rigtige første sted at kigge.

## Trin 9: Skalering

```bash
kubectl scale deployment flask-demo --replicas=3 -n workshop
kubectl get pods -n workshop
```

Nu kan du se, at Kubernetes holder tre ens pods koerende bag samme service.

## Trin 10: Ryd op

Slet workloaden:

```bash
kubectl delete -f examples/flask-demo/k8s
```

Slet clusteret:

```bash
kind delete cluster --name workshop
```

## Ekstra oevelse: Fra Compose til Kubernetes

I [examples/flask-postgres/k8s](/home/kasc/projects/k8s-session/aka-docker-local-k8s/examples/flask-postgres/k8s) ligger et bevidst simpelt eksempel paa samme app som i Compose-udgaven.

Det er ikke et produktionssetup. Det er et laeringssetup.

Ting du kan kigge efter:

- Hvordan `db` i Compose bliver til en `Service`
- Hvordan miljoevariabler flytter over i manifests
- Hvorfor persistence hurtigt bliver et stoerre emne i Kubernetes

## Tjekliste

### Docker
- [ ] Koere `hello-world`
- [ ] Bygge et image lokalt
- [ ] Starte en Flask-app i Docker
- [ ] Forstaa forskellen paa volume og bind mount
- [ ] Koere flere services med Compose

### Kubernetes lokalt
- [ ] Installere `kubectl` og `kind`
- [ ] Oprette et lokalt cluster
- [ ] Loade et image ind i `kind`
- [ ] Deploye med `kubectl apply`
- [ ] Bruge `port-forward`
- [ ] Laese logs og events
- [ ] Skalere en deployment
- [ ] Slette clusteret igen

## Hvad blev ikke daekket?

- Ingress controllers
- Persistent volumes i dybden
- Helm charts
- ConfigMaps og Secrets i mere realistiske setups
- Health checks og probes
- CI/CD
- Managed Kubernetes som AKS, EKS eller GKE

Det er bevidst. Foerst giver det mening at forstaa de lokale grundbegreber.

Hvis du senere vil videre, er den naturlige progression:

1. Lokal Docker
2. Lokal Kubernetes med `kind`
3. Mere realistiske manifests
4. Helm
5. Managed Kubernetes

## Sektion 3: Bonus - fra `kind` til vores egen Talos-platform

`kind` er godt til at laere Kubernetes-begreberne hurtigt. Vores egen lokale platform er noget andet. Den handler ikke kun om at koere pods, men ogsaa om at bygge og drive selve clusteret.

Det er den vigtigste forskel:

- I `kind` faar du et faerdigt cluster med det samme
- I Talos-setuppet bygger vi clusteret bevidst op fra bunden

Denne del er inspireret af vores setup i [DevOps-kubernetes-master](/home/kasc/projects/DevOps-kubernetes-master).

## Den mentale overgang

Hvis du har lavet ovelserne ovenfor, kender du allerede de vigtigste Kubernetes-objekter:

- `Deployment`
- `Pod`
- `Service`
- `Namespace`

I vores Talos-setup arbejder vi et niveau under det:

- Hvordan control planes bliver oprettet
- Hvordan worker nodes bliver oprettet
- Hvordan clusteret bliver bootstrapped
- Hvordan API endpoint og netvaerk bliver gjort stabile
- Hvordan basis-komponenter som Cilium bliver installeret

Kort sagt:

- Workshop del 1 og 2 handler om workloads i Kubernetes
- Bonusdelen handler om selve Kubernetes-platformen

## Hvordan vores setup er bygget op

Det overordnede flow ligger i [cluster.yml](/home/kasc/projects/DevOps-kubernetes-master/ansible/playbooks/cluster.yml).

Her er ideen:

1. Talos-infrastruktur bliver provisioneret
2. Talos bliver opgraderet hvis det er noedvendigt
3. Kubernetes-services bliver deployet bagefter

Det er en vigtig opdeling, fordi den skiller platform fra workloads.

- Platform er fx noder, bootstrap, netvaerk og kubeconfig
- Workloads er fx services, controllers og applikationer

## Hvad sker der i praksis?

Provisioneringsflowet ligger i [deploy-infra.yml](/home/kasc/projects/DevOps-kubernetes-master/ansible/playbooks/talos/deploy-infra.yml).

Det kan laeses som fire hovedtrin:

1. Der laves nye Talos-secrets til personlige clusters
2. Control plane-noder bliver oprettet
3. Clusteret bliver bootstrapped
4. Worker-noder og basis-services bliver gjort klar

Det er meget taettere paa et rigtigt cluster-livscyklusforloeb end `kind`.

## Control plane og worker nodes

I workshoppen saa du pods og deployments. I Talos-setuppet skal vi foerst have maskinerne.

Control plane provisioning sker i [control-plane/tasks/main.yml](/home/kasc/projects/DevOps-kubernetes-master/ansible/roles/hypervisor/talos-vm/control-plane/tasks/main.yml).

Der sker blandt andet dette:

- Der genereres Talos machineconfig med `talosctl gen config`
- Der patches netvaerk og hostname ind
- Konfigurationen bliver lagt ind som VM boot-parameter
- VM'en bliver oprettet i vSphere

Worker provisioning i [worker-node/tasks/main.yml](/home/kasc/projects/DevOps-kubernetes-master/ansible/roles/hypervisor/talos-vm/worker-node/tasks/main.yml) foelger samme moenster, men med worker-konfiguration.

Det er den konkrete version af:

- `kind`: "lav et cluster"
- Talos-platform: "byg de maskiner clusteret koerer paa"

## Bootstrap: hvornår bliver det til et rigtigt cluster?

Det step ligger i [bootstrap/tasks/main.yml](/home/kasc/projects/DevOps-kubernetes-master/ansible/roles/talos/bootstrap/tasks/main.yml).

Her bliver en control plane node brugt til at bootstrappe clusteret, og de andre control planes bliver bagefter koblet paa.

Det er et godt sted at forbinde teori og praksis:

- Kubernetes API findes ikke rigtigt foer bootstrap
- `kubectl` giver foerst mening naar control plane er oppe
- Et HA-control-plane er ikke bare "flere VM'er", men en samlet kontrolflade

## VIP og stabil API-adgang

I `kind` taenker man ikke saa meget over API-endpointet. I et rigtigt setup betyder det mere.

I [configure-vip/tasks/main.yml](/home/kasc/projects/DevOps-kubernetes-master/ansible/roles/talos/configure-vip/tasks/main.yml) bliver control plane-konfigurationen patched, saa API'et peger paa en virtuel IP.

Det loeser et konkret problem:

- Du vil ikke binde din kubeconfig og dine tools til en enkelt control plane node
- Du vil have et stabilt endpoint selv hvis en node forsvinder

Det er samme slags stabilitetsprincip som en Kubernetes `Service` giver workloads, bare paa clusterets egen kontrolflade.

## CNI og netvaerk: hvorfor Cilium betyder noget

I workshoppen brugte du `Service` og port-forward uden at skulle taenke saerligt over underliggende netvaerk. I vores platform er det en bevidst del af setup'et.

I [cilium/tasks/main.yml](/home/kasc/projects/DevOps-kubernetes-master/ansible/roles/talos/cilium/tasks/main.yml) bliver Talos patched, saa standard-CNI og `kube-proxy` ikke bruges, og derefter bliver Cilium installeret.

Det er vigtigt af to grunde:

- Pods skal kunne tale sammen
- Services skal kunne rout'es stabilt

Det er med andre ord den del, der goer at dine workloads faktisk kan opfoere sig som et cluster og ikke bare som isolerede containere.

## `kubeconfig` og `talosconfig`

I `kind` faar du meget foraeret. I Talos-setuppet er klientkonfiguration en tydeligere del af flowet.

`Justfile` i [Justfile](/home/kasc/projects/DevOps-kubernetes-master/Justfile) viser det ret godt:

- `just kubeconfig ...` genererer adgang til Kubernetes
- `just deploy-personal <initialer>` koerer hele det personlige clusterflow
- `just reset-personal <initialer>` rydder lokal Talos- og kubeconfig-state op

Det er nyttigt at skelne mellem:

- `kubeconfig`: hvordan du snakker med Kubernetes API
- `talosconfig`: hvordan du administrerer selve Talos-noderne

Den skelnen findes ikke i den simple `kind`-oevelse, men den er vigtig i et mere realistisk setup.

## Hvordan bonusdelen haenger sammen med workshoppen

Her er den korte mapping:

- `docker run` laerer dig hvad en container er
- `docker compose` laerer dig hvad flere services er
- `kind` laerer dig de vigtigste Kubernetes-objekter
- Talos-setuppet laerer dig hvordan clusteret bag objekterne bliver skabt og drevet

Det vil sige:

- Sektion 1: containere
- Sektion 2: workloads i Kubernetes
- Sektion 3: platformen der koerer Kubernetes

## Hvis du vil koble det til vores egen hverdag

Naar du arbejder i det rigtige setup, kan du taenke saadan her:

- Hvis problemet handler om pods, services, namespaces eller logs, er du i workload-laget
- Hvis problemet handler om node bootstrap, Talos config, VIP eller Cilium, er du i platform-laget

Den opdeling goer debugging og ansvar meget mere overskueligt.

## Forslag til videre bonus-oevelser

1. Laes [deploy-infra.yml](/home/kasc/projects/DevOps-kubernetes-master/ansible/playbooks/talos/deploy-infra.yml) og identificer hvor control plane, bootstrap og worker provisioning sker.
2. Laes [cluster.yml](/home/kasc/projects/DevOps-kubernetes-master/ansible/playbooks/cluster.yml) og forklar forskellen paa platform deployment og service deployment.
3. Laes [cilium/tasks/main.yml](/home/kasc/projects/DevOps-kubernetes-master/ansible/roles/talos/cilium/tasks/main.yml) og forklar hvorfor netvaerk ikke bare er en detalje i Kubernetes.
4. Laes [bootstrap/tasks/main.yml](/home/kasc/projects/DevOps-kubernetes-master/ansible/roles/talos/bootstrap/tasks/main.yml) og forklar hvorfor bootstrap kun maa ske fra en control plane node ad gangen.
