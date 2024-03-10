# Exploring ARM Architecture: A Practical Demo with Python API on EKS

This blog post is intended for individuals interested in exploring the intricacies of ARM architecture, particularly software developers seeking to understand its capabilities within the context of Kubernetes orchestration.

## What will you learn?

By the end of this post, you will gain insights into:

- Exploring the fundamentals of ARM architecture
- Build arm64 container image with docker buildx.
- Utilizing a Python API to convert MKV videos to MP3 audio files
- Orchestrating tasks seamlessly on EKS
- Demonstrating its potential through a captivating demo

## Prerequisites

- Git installation is necessary to clone my repository.
- A computer capable of running Docker, supported on Windows, macOS, or Linux, regardless of architecture.
- To work with the Amazon EKS clusters, ensure that both the eksctl and kubectl are installed and configured locally.
- A Docker Hub account
- An AWS account is required to deploy and access resources.

## A Quick Introduction to Arm-based (Graviton) Processors

Arm-based [Graviton](https://aws.amazon.com/ec2/graviton/) processors have been gaining significant attention in recent years, and for good reason. What sets them apart is their innovative architecture, which is designed to offer superior performance, efficiency, and scalability compared to traditional x86 processors. With a focus on energy efficiency and high-performance computing, Arm-based processors are revolutionizing the landscape of computing devices, from mobile phones to data centers.

## Cloning the Github Repository for Quick Setup

To simplify things, you can clone the code directly from my repository. Follow these steps:

Clone the repository containing the Python API code to your local machine.

```bash
git clone https://github.com/sprider/eks-arm-python-mkvtomp3convertor.git
```

Move into the cloned repository directory.

```bash
cd eks-arm-python-mkvtomp3convertor
```

## Building Our Amazon EKS Cluster

To kickstart our journey into modern computing with ARM architecture, we begin by setting up an Amazon EKS cluster.

First, we create the EKS cluster using eksctl and a configuration file (cluster.yaml).

```sh
eksctl create cluster -f cluster.yaml
```

After creating the cluster, verify that the nodes are up and running using kubectl.

```sh
kubectl get nodes
```

Run this command to determine the architecture of the nodes:

```sh
kubectl get node -o jsonpath='{.items[*].status.nodeInfo.architecture}'
```

## Build multi-architecture docker images with docker buildx

Now, let us pack our Python API into a Docker container. Docker containers make it super easy to run our Python API on any computer, whether x86 or new ARM-based ones.

To build multi-architecture Docker images using Docker Buildx and push them to your repository, follow these steps:

Sign in to Docker Hub and create a new repository with your chosen name. Then, run the following command, and enter your Docker Hub username and password when prompted:

```sh
docker login
```

Create a new Docker Buildx instance named "eks-arm" and set it as the active instance:

```sh
docker buildx create --name eks-arm --use --bootstrap
```

Build the Docker image using the specified tags and platforms:

Replace "your-repo-name" in the command above with the name of your Docker Hub repository.

```sh
docker buildx build -t your-repo-name:latest --platform linux/arm64 --push .
```

After executing the above commands, you should find the Docker image in your Docker Hub repository.

## Deploying Kubernetes service in EKS cluster

To deploy the application, you can use the provided Kubernetes manifest file k8s-app-deployment.yaml. This file contains the necessary specifications for deploying the application in your EKS cluster. Open the k8s-app-deployment.yaml file in a text editor and replace your-repo-name:latest with your own Docker image reference. This should be the name of your Docker Hub repository and the tag of the image.

Apply the manifest to your EKS cluster using the following command:

```sh
kubectl apply -f k8s-app-deployment.yaml
```

After applying the manifest, ensure the service type has changed to NodePort and the deployment is successful. Check the status of your deployments with:

```sh
kubectl get deployments
```

Make sure the deployment eks-arm-python-mkvtomp3convertor-app is listed with the desired number of replicas.

Run the following command to retrieve the IP addresses of the nodes in your EKS cluster:

```sh
kubectl get nodes -o wide
```

Run the following command to retrieve the NodePort assigned to the eks-arm-python-mkvtomp3convertor-service.

```sh
kubectl get svc eks-arm-python-mkvtomp3convertor-service -o=jsonpath='{.spec.ports[0].nodePort}'
```

Construct the URL using the Node's IP address and assigned NodePort: http://node-ip:node-port. Remember to open the NodePort in the security group linked with your EKS nodes to permit incoming traffic. Now, your application is accessible using this URL.

## Calling Our Service with Curl

To test the service using curl and a sample mkv file, follow these instructions:

Ensure you have a sample mkv file named sample.mkv available on your local system.

Execute the following curl command to send a POST request with the sample MKV file to the service for conversion:

```sh
curl -X POST -F "video=@/path/to/sample.mkv" http://node-ip:node-port/convert --output /path/to/converted_audio.mp3
```

- Replace /path/to/sample.mkv with the actual path to your sample.mkv file.
- Replace node-ip and node-port with the IP address of one of your EKS cluster nodes and the assigned NodePort for the service, respectively. You can obtain these values using the commands provided earlier.
- Replace /path/to/converted_audio.mp3 with the desired location where you want to save the converted audio file.

After executing the curl command, wait for the conversion process to complete. The converted audio file will be saved to the specified output location.

Once the conversion is finished, verify that the audio file converted_audio.mp3 has been created at the specified output location.

And there you have it, folks! We have taken a fun and straightforward journey into ARM architecture with our Python API experiment. With ARM-based computers, along with excellent tools, we have seen how easy it is to explore the future of computing. So, keep experimenting, keep exploring, and who knows what amazing things we will discover next!
