# SOLUTIONS


## Objective
Describe solutions for each exercise of the [DevSecOps&#32;tech&#32;case.pdf](./DevSecOps&#32;tech&#32;case.pdf) document.


## Overview
The solutions were deployed and tested using the following sw/tools:

- Docker:   `v20.10.21`
- kubectl:  `v1.26.1`
- Minikube: `v1.32.0`
- Kubernetes: `v1.28.3`
- Python:   `v3.12.0`
- Ubuntu: `v18.04.6 LTS (Bionic Beaver)`


## 1.1 Install and configure Docker

Create Ansible playbook site.yml that will:

- Install the Docker service
- Enable container logging to Docker host’s syslog file


```
Example of expected result:
$ docker
The program 'docker' is currently not installed. You can install it by
typing:sudo apt install docker.io
$ ansible-playbook -i "localhost," -c local site.yml
<...snip...>
$ docker -v
Docker version 17.12.0-ce, build c97c6d6
$ docker info | grep 'Logging Driver'
Logging Driver: syslog
```



### Solution
![Ansible](./logos/ansible.png)


Two files were created for this solution:


1. The file [site.yml](./1.1-ansible/site.yml) contains the playbook to install docker on an ubuntu 18.04 machine.
2. The file [daemon_config.j2](./1.1-ansible/daemon_config.j2) contains the parameters to set the `Logging Driver: syslog`.

Scope:
- The solution only focus on the installation of docker packages and configure docker for the first time on the machine.
- The solution does not cover the scenario where docker is already installed and the configuration changes or additional packages must be install.



## 1.2 Write a weather reporting program

Create a simple script getweather that will get the current weather from
https://openweathermap.org/api (you can use a library like pyowm).

The script reads no CLI arguments. It is parametrized via the following environment

variables: OWM_API_KEY, OWM_CITY. It prints to stdout.

```
Example of expected results:
$ export OWM_API_KEY='xxxx'
$ export OWM_CITY='Honolulu'
$ ./getweather
city="Honolulu", description="few clouds", temp=70.2, humidity=75
```



### Solution
![Python](./logos/python.png)


The file [getweather](./1.2-getweather/getweather) contains the python3 script to get the data requested.

Scope:
- The solution assumes python module `requests` is already installed


```
# Output

$ ./getweather 
city="Honolulu", description="scattered clouds", temp=299.4, humidity=79

```

## 1.3 Dockerize and run the program

Create Dockerfile for building image for the getweather program you’ve written.

Then build and run the image.

```
Example of expected result:
$ docker run --rm -e OWM_API_KEY="xxxx" -e OWM_CITY="Honolulu" getweather:dev
$ grep -i honolulu /var/log/syslog
Nov 30 11:50:07 ubuntu-vm ae9395e86676[1621]: city="Honolulu",
description="few clouds", temp=70.2, humidity=75
```

### Solution
![Docker](./logos/docker.png)


The [Dockerfile](./1.3-docker-image/Dockerfile) contains all instructions to create a docker image using as a base `python:3-alpine` as is already a downsized image.



```
# build the image on my local machine


$ docker build -t getweather:dev .
Sending build context to Docker daemon  4.608kB
Step 1/8 : FROM python:3-alpine
 ---> 5f9e8f452a5c
Step 2/8 : ENV OWM_CITY Honolulu
 ---> Using cache
 ---> c8d11454857f
Step 3/8 : ENV OWM_API_KEY xxxxxxxxxxx
 ---> Running in 570853ea24dc
Removing intermediate container 570853ea24dc
 ---> 7add1801cbb1
Step 4/8 : WORKDIR /app
 ---> Running in 0425998614a8
Removing intermediate container 0425998614a8
 ---> 4b174d77ce39
Step 5/8 : COPY requirements.txt ./
 ---> 42f6d1cdc6f6
Step 6/8 : RUN pip install -r requirements.txt
 ---> Running in 8d5d7290898d
 ---> 98f768c88aaf
Step 7/8 : COPY getweather.py ./
 ---> 3926807ea27f
Step 8/8 : CMD [ "python", "getweather.py" ]
 ---> Running in 878d0494174a
Removing intermediate container 878d0494174a
 ---> 7265da685069
Successfully built 7265da685069
Successfully tagged getweather:dev

# The `OWM_API_KEY` was obfuscated
$ docker run --rm -e OWM_API_KEY="xxxxxxxxxxxxxxxxxxxxx" -e OWM_CITY="Honolulu" getweather:dev
city="Honolulu", description="few clouds", temp=299.86, humidity=78


```



## 2.1 Write a network scanner

Write a program for repetitive network scans that will display differences between
scans.

Scan can be executed either using external tools or dedicated libraries of
the selected programming language.

- Target of the scan must be parametrized as CLI argument
- Target can be single IP address as well as network range

```
Example of expected result:
$ ./scanner 10.1.1.1
10.1.1.1
* 22/tcp open
* 25/tcp open
```

### Solution
![Python](./logos/python.png)


The file [scanner](./2.1-scanner/scanner) contains the python3 script to scan an specific IP or a Network range using CIDR block format as an argument.

Scope:
- The solution assumes `nmap` package is already installed.


```
# Scan specific IP

$ ./scanner 192.168.1.39

Nmap scan report for 192.168.1.39
PORT     STATE SERVICE
22/tcp   open  ssh
5901/tcp open  vnc-1
6001/tcp open  X11:1


# Scan network range using CIDR block format

$ ./scanner 172.17.0.0/24

Nmap scan report for 03984njcjknvnbh48fh (172.17.0.1)
PORT     STATE SERVICE
22/tcp   open  ssh
25/tcp   open  smtp
80/tcp   open  http
5000/tcp open  upnp
8080/tcp open  http-proxy
9090/tcp open  zeus-admin

Nmap scan report for 172.17.0.2
PORT     STATE SERVICE
22/tcp   open  ssh
8081/tcp open  blackice-icecap

Nmap scan report for 172.17.0.3
PORT     STATE SERVICE
5000/tcp open  upnp

```


## 2.2 Kubernetize and deploy the scanner

Create Docker image containing the scanner program and push it to a public
repository like Docker Hub.

Create Kubernetes manifest that will run the image periodically every 5 minutes.

Install local Kubernetes like minikube and apply the manifest.

```
Example of expected result:
$ kubectl apply -f scanner.yaml
$ kubectl get cj

NAME      SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
scanner   0 5 * * *     False     0        7m              13m

```

### Solution
![Kubernetes](./logos/kubernetes.png)


For this scenario 3 files are part of the solution:

1. The file [scanner.py](./2.2-kubernetes/scanner.py) contains the scanner app python3 code.
2. The file [Dockerfile](./2.2-kubernetes/Dockerfile) contains the instructions to build the docker image which contains the scanner app.
3. The file [cronjob.yaml](./2.2-kubernetes/cronjob.yaml) contains the k8s cronjob resource manifest to run every 5 minutes.


Scope:
- The docker image scans the following CIDR block `10.244.0.0/24` by default
- The cronjob is created in the `default` namespace
- For the cronjob resoure the following parameters were set:
  - `concurrencyPolicy: Forbid`: Disable to trigger a new job if the previous job still running.
  - `restartPolicy: Never`: The container won't be restarted.
  - `backoffLimit: 0`: Job will run only once.



```

# build the image on my local machine and push it into my Dockerhub account and set it as `Public` available
docker build -t scanner .
docker login
docker tag 0c8565a1cae1 mauriche/scanner:latest
docker push mauriche/scanner:latest



# Use kubectl to create scanner cronjob k8s resource

$ kubectl apply -f cronjob.yaml
cronjob.batch/scanner created

$ kubectl get cj
NAME      SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
scanner   */5 * * * *   False     0        3m40s           89m

$ kubectl get pods
NAME                     READY   STATUS      RESTARTS   AGE
scanner-28360585-kkqzt   0/1     Completed   0          13m
scanner-28360590-qwr7l   0/1     Completed   0          8m46s
scanner-28360595-tdqbf   0/1     Completed   0          3m46s

$ kubectl logs scanner-28360585-kkqzt
Nmap scan report for 10.244.0.1
PORT     STATE SERVICE
22/tcp   open  ssh
8443/tcp open  https-alt

Nmap scan report for coredns-5dd5756b68-hthgw (10.244.0.39)
PORT     STATE SERVICE
53/tcp   open  domain
8080/tcp open  http-proxy
8181/tcp open  intermapper


```

