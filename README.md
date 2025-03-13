# kuBERTnetes - Parity Takehome

The goal of this exercise is to build a basic [Kubernetes](https://kubernetes.io/docs/concepts/overview/) debugger using LLMs that we're going to call kuBERTnetes.
Kubernetes is a massively popular container orchestration tool that is used by many of the services you use every day. Individual applications can be
run as microservices in a Kubernetes cluster, and Kubernetes will manage the deployment, scaling, and networking between them. This allows it to handle massive
scale with high availability. However, Kubernetes deployments can become complex and difficult to debug due to their stateless nature.

We're going to run a basic Kubernetes cluster locally using [k3d](https://k3d.io/stable/) and deploy a basic pre-written application to it. The pre-written application
includes an intentional fault. You'll then create kuBERTnetes, a tool that should be able to diagnose the issue and suggest a fix.

## Setup

If you have a Windows machine, please email me because these steps might not work for you.

### k3d

Follow the instructions in the `k3d-cluster/README.md` file to get the cluster running. You should see the following output from `kubectl get pods`:

```bash
NAME                             READY   STATUS             RESTARTS   AGE
crashloop-app-<POD_ID>           0/1     CrashLoopBackOff   15         7m58s
faulty-app-<POD_ID>              2/2     Running            0          7m55s
```

You can port forward the faulty-app service to your local machine to view the status page:

```bash
kubectl port-forward service/faulty-app-service 8080:80
```

You can visit `localhost:8080` to view the status page and see that the application has a bad status.

## Task

The basic implementation of kuBERTnetes will be a CLI tool (or a similar interface) that allows you to ask questions about the Kubernetes cluster. It should allow us to chat back and forth with kuBERTnetes to understand the state of the cluster and diagnose issues. The experience would look something like this:

```bash
$ ./kuBERTnetes

Welcome to kuBERTnetes!

> Why is the application served by my pod not working?

Checking the status of your pods...

etc...
```

You are free to implement this with any language and tools you'd like.

Here are the basic requirements:

- The tool should be easy to run and use.
- It should be able to query the state of the cluster.
- It should be able to diagnose issues with the cluster.
- It should be able to suggest fixes for issues.

To give a brief overview of how we understand the state of Kubernetes clusters, let me outline some concepts. A Kubernetes cluster has a few key concepts. First, there is the concept of the control plane and the data plane. Kubernetes is an orchestation tool, so the control plane is responsible for making decsions about the cluster regarding the allocation of resources, scheduling, and other cluster-wide choices. The data plane is the part of the cluster that is actually running the applications. We define what we want a cluster to look like using a YAML file, which we call a "manifest". We then apply the manifest to the cluster using `kubectl apply -f <manifest>.yaml`. This defines what our desired application state is and then the control plane will start to make the necessary changes to the cluster to reach that state.

In our manifest, we define applications as a collection of containers that run together in a shared environment, called a namespace. They can network with each other, share volumes of disk space, and lots of other interesting stuff we don't need to get into now. When we apply the manifest to the cluster, the control plane will start to run the containers defined in the manifest in pods. Pods ultimately run on cluster level nodes, which are just the physical or virtualized machines that the cluster is running on.

In our case, we're running a lightweight wrapper on a minimal Kubernetes cluster using a tool called k3d as mentioned above. We start the cluster up and it's automatically provisioned some resources and has a running control plane. We'll then apply the manifest to get our application running on the cluster. In the deployment we're running (in `k3d-cluster/faulty-deploy.yaml`), we're running a couple of contianers, both with some intentional faults.

In order to allow an LLM to access the state of the cluster, we need to provide the LLM with the ability to run `kubectl` commands. `kubectl` includes access control as well, but if we run it locally, we should be fine as we already have access to our own cluster. Providing this as a tool call to the LLM should allow it to query the state of the cluster and hopefully then diagnose issues.

## Extensions

- _Add a tool call to allow the LLM to retrieve Kubernetes documentation._
  If we provide the LLM with access to the Kubernetes documentation, it should be better at answering questions about the state of the cluster and suggesting fixes. To do this, you can provide the documentation via RAG. You would need to set up a vector database where you store the embeddings of the documentation, and then use a similarity search to find the most relevant documentation for a given question.
- _Create an evaluation suite to test the accuracy of the LLM's diagnosis._
  We could create a basic evaluation suite to test the accuracy of the LLM's diagnosis. This suite should provide a set of issues to the LLM where we have a known correct diagnosis. We can then run the LLM and compare its diagnosis to the known correct diagnosis. There are levels to how strong an evaluation suite we can create. The ideal version is one where the LLM can fully query the state of the cluster.
- _Create a web interface for kuBERTnetes._
  We could create a basic web interface for kuBERTnetes that allows us to interact with the LLM in a more user-friendly way. If you wanted to stay exclusively within Python, you could use Flask or FastAPI to create a basic webapp. If you wanted to use some additional frameworks, you could use Python as the backend and use a NextJS frontend.

## Evaluation

After you are finished implementing your solution, please record a Loom video walking through both using the tool and your implementation of the tool. The more depth you're able to go into, the better - especially on any extensions you've implemented. Please email me a link to the Loom as well as a zip of the project directory.

Good luck!
