# Section 3 slide notes

Section 3 should stay practical. The goal is not to explain all of Talos or all of our cluster platform. The goal is to make participants comfortable using our repo to create and access a personal cluster.

## Suggested scope

Focus on:

- what Talos is at a high level
- what a personal cluster is in our setup
- the difference between control plane and worker nodes
- what `kubeconfig` and `talosconfig` are
- which `just` commands participants need
- the happy-path workflow
- what to do when they need to reset and try again

Avoid going deep on:

- Talos bootstrap internals
- VIP details
- deep Cilium details
- full Ansible implementation flow
- upgrade internals

## Suggested slide structure

### 1. From `kind` to our real setup

Purpose:

- connect section 2 to section 3
- explain that participants are now moving from a learning cluster to the team setup

Points:

- section 2 was about learning Kubernetes concepts locally
- section 3 is about using our repo to spin up a personal cluster
- the goal is to use the platform, not understand every implementation detail

### 2. Talos in one slide

Purpose:

- give just enough context that the repo commands do not feel magical

Points:

- Talos is the platform/OS layer for Kubernetes nodes
- it is designed for running Kubernetes
- you manage the cluster through tooling and configuration rather than manual server tinkering
- for this workshop we only need a few concepts

### 3. Concepts you need

Purpose:

- define the terms participants will see in the repo and commands

Points:

- control plane: runs the Kubernetes control components
- worker node: runs your workloads
- personal cluster: your own isolated cluster in the shared setup model
- `kubeconfig`: used with `kubectl` to talk to Kubernetes
- `talosconfig`: used with `talosctl` to talk to Talos nodes

### 4. The commands you will use

Purpose:

- narrow attention to the commands participants actually need

Points:

- `just deploy-personal <initials>`
- `just kubeconfig ...` if that is needed in the workshop flow
- `just reset-personal <initials>`

Suggested framing:

- `deploy-personal` creates or converges your personal cluster
- `kubeconfig` gives you local access to the cluster
- `reset-personal` is the clean retry path when state gets messy

### 5. Happy path

Purpose:

- show the intended workflow from start to first successful verification

Points:

- clone the repo
- run the personal cluster command
- wait for provisioning to complete
- get cluster access
- verify with `kubectl get nodes`
- continue with normal Kubernetes usage

### 6. If something goes wrong

Purpose:

- reduce fear and give a practical recovery path

Points:

- local Talos or kubeconfig state can get out of sync
- use the reset flow
- rerun the deploy command
- ask for help when provisioning fails in ways the workshop does not cover

## Recommended talk track

Keep the talk track short:

- in section 2 you learned what Kubernetes objects look like from the user side
- in section 3 you use our real repo to get a personal cluster
- you do not need to understand every role or playbook to be productive
- you do need to understand the basic terms and the small set of `just` commands

## Recommended slide count

Aim for 5 to 6 slides total.

If time is tight, compress to 4 slides:

1. why section 3 exists
2. Talos and the core concepts
3. the commands you will use
4. happy path and reset path

## Suggested demo tie-in

If you demo live, keep it simple:

1. show the repo
2. point out the `Justfile`
3. run or discuss `just deploy-personal <initials>`
4. show the verification step with `kubectl get nodes`
5. mention `just reset-personal <initials>` as the fallback
