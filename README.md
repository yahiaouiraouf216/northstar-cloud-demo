# Northstar Cloud Demo 🚀

A production-style DevOps portfolio project demonstrating how to build, containerize, provision, secure, and automatically deploy a Python Flask application on AWS.

The project uses **Terraform, Docker, Docker Compose, GitHub Actions, AWS EC2, AWS SSM, S3 and Checkov** to implement an automated CI/CD workflow.

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │       Developer     │
                    │     Git push main   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     GitHub Actions   │
                    │       CI/CD          │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
             Python Test    Docker Build   Terraform
                              & Push       Plan/Apply
                 │             │             │
                 │             ▼             ▼
                 │        Docker Hub       AWS
                 │                            │
                 │                            ▼
                 │                         EC2
                 │                            │
                 │                           SSM
                 │                            │
                 │                            ▼
                 │                    Docker Container
                 │                            │
                 └────────────────────────────┤
                                              ▼
                                      Flask Application
                                              │
                                              ▼
                                           HTTP :80
```

---

## 🛠️ Technologies

| Technology     | Purpose                       |
| -------------- | ----------------------------- |
| Python / Flask | Web application               |
| Docker         | Application containerization  |
| Docker Compose | Local container orchestration |
| Terraform      | Infrastructure as Code        |
| AWS EC2        | Application server            |
| AWS VPC        | Network infrastructure        |
| AWS IAM        | Access management             |
| AWS SSM        | Secure remote management      |
| AWS S3         | Terraform remote state        |
| AWS CloudWatch | Logging infrastructure        |
| GitHub         | Source control                |
| GitHub Actions | CI/CD automation              |
| Docker Hub     | Container image registry      |
| Checkov        | Terraform security scanning   |

---

## 📁 Project Structure

```text
northstar/
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── templates/
│       ├── index.html
│       └── status.html
│
├── docker/
│   └── Dockerfile
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── user_data.sh
│   └── backend.tf
│
├── .github/
│   └── workflows/
│       └── cicd.yml
│
├── .checkov.yaml
├── docker-compose.yml
└── README.md
```

---

# 🚀 Application

The project contains a small Flask application used to demonstrate the complete DevOps workflow.

### Available endpoints

```text
/
```

Main application page displaying application information.

```text
/status
```

Application status page.

```text
/health
```

Health endpoint returning JSON information.

Example:

```json
{
  "status": "ok",
  "hostname": "container-id"
}
```

---

# 🐳 Docker

The Flask application is containerized using Docker.

### Build the image

```bash
docker build -f docker/Dockerfile -t northstar-app .
```

### Run the container

```bash
docker run -d \
  --name northstar-app \
  -p 5000:5000 \
  northstar-app
```

The application is then available at:

```text
http://localhost:5000
```

---

# 🐳 Docker Compose

Docker Compose is used to simplify local application management.

### Start the application

```bash
docker compose up -d
```

### Check the container

```bash
docker compose ps
```

### View logs

```bash
docker compose logs
```

### Stop the application

```bash
docker compose down
```

The Compose configuration automatically exposes:

```text
localhost:5000
```

and uses:

```yaml
restart: unless-stopped
```

to automatically restart the container when appropriate.

---

# ☁️ AWS Infrastructure

The infrastructure is provisioned using Terraform.

The project creates:

* VPC
* Public subnet
* Internet Gateway
* Route table
* Security Group
* EC2 instance
* IAM role
* IAM instance profile
* AWS Systems Manager access
* CloudWatch log group
* VPC Flow Logs
* S3 remote Terraform state

### Network

```text
VPC
10.0.0.0/16
│
└── Public Subnet
    10.0.1.0/24
    │
    └── EC2
```

The EC2 instance runs the Dockerized Flask application.

---

# 🏗️ Terraform

Terraform is used as Infrastructure as Code to create and manage the AWS environment.

### Initialize Terraform

```bash
cd terraform
terraform init
```

### Format Terraform files

```bash
terraform fmt
```

### Validate configuration

```bash
terraform validate
```

### Create an execution plan

```bash
terraform plan
```

### Apply infrastructure

```bash
terraform apply
```

### Destroy infrastructure

```bash
terraform destroy
```

> `terraform destroy` should only be used when the AWS infrastructure is no longer required.

---

# 🗄️ Terraform Remote State

Terraform state is stored remotely in an AWS S3 bucket.

This allows the local environment and GitHub Actions to work with the same Terraform state.

Example backend configuration:

```hcl
terraform {
  backend "s3" {
    bucket = "northstar-terraform-state-557629718261"
    key    = "northstar/terraform.tfstate"
    region = "us-east-1"
  }
}
```

The Terraform state file is therefore not stored in the Git repository.

---

# 🔐 Security

Checkov is integrated into the CI/CD pipeline to scan the Terraform configuration for security issues.

Example:

```bash
checkov -d terraform
```

The project also implements:

* IMDSv2 on EC2
* IAM role for EC2
* AWS Systems Manager instead of SSH
* Restricted inbound traffic
* Terraform security scanning
* Remote Terraform state
* GitHub Secrets for AWS and Docker Hub credentials

Some Checkov rules are explicitly skipped because this is a small portfolio/demo environment and certain controls would add unnecessary cost or complexity.

---

# 🔄 CI/CD Pipeline

GitHub Actions automatically runs when changes are pushed to `main`.

Pipeline:

```text
Git Push
   │
   ▼
Python Tests
   │
   ├───────────────┐
   ▼               ▼
Docker          Terraform
Build/Push       Validation
   │               │
   │            Checkov
   │               │
   │            Terraform
   │              Plan
   │               │
   └───────┬───────┘
           ▼
        Deploy
           │
           ▼
       AWS EC2
           │
           ▼
    Docker Container
```

### CI checks

The pipeline performs:

1. Checkout source code
2. Install Python dependencies
3. Validate Python application
4. Build Docker image
5. Push image to Docker Hub
6. Initialize Terraform
7. Format check
8. Terraform validation
9. Checkov security scan
10. Terraform plan
11. Terraform apply
12. Deploy the latest Docker image to EC2 using AWS Systems Manager

---

# 🐳 Docker Hub

The application image is published to Docker Hub:

```text
yahiaouiraouf/northstar-app:latest
```

GitHub Actions automatically builds and pushes the image when changes are pushed to `main`.

---

# 🚀 Deployment

After a successful CI/CD pipeline:

```text
GitHub
   │
   ▼
GitHub Actions
   │
   ▼
Docker Hub
   │
   ▼
AWS SSM
   │
   ▼
EC2
   │
   ▼
Docker
   │
   ▼
Flask Application
```

The EC2 deployment pulls the latest image and starts the container with:

```text
--restart unless-stopped
```

The application is exposed on HTTP port `80`.

---

# 🧪 Local Testing

Start the application:

```bash
docker compose up -d
```

Verify:

```bash
docker compose ps
```

Test the application:

```bash
curl http://localhost:5000
```

Test the health endpoint:

```bash
curl http://localhost:5000/health
```

Stop the application:

```bash
docker compose down
```

---

# 📊 DevOps Concepts Demonstrated

This project demonstrates practical experience with:

* Infrastructure as Code
* Cloud infrastructure
* AWS networking
* IAM
* EC2
* Systems Manager
* Docker
* Docker Compose
* Container registries
* CI/CD
* GitHub Actions
* Terraform remote state
* Infrastructure validation
* IaC security scanning
* Automated deployment
* Application health checks
* Troubleshooting containers and cloud infrastructure

---

# 🎯 Project Objectives

The objective of Northstar was to simulate a simplified real-world DevOps workflow:

> **Developer → GitHub → CI/CD → Docker → Terraform → AWS → Deployment**

The project focuses on automation, reproducibility, infrastructure management and deployment rather than application development.

---

# 📌 Future Improvements

Possible improvements for a future version:

* Kubernetes deployment
* HTTPS with TLS
* Application Load Balancer
* Route 53
* AWS Secrets Manager
* GitHub Actions OIDC authentication
* Terraform modules
* Automated integration tests
* Container vulnerability scanning
* Prometheus / Grafana monitoring
* Blue/Green or Rolling deployments

---

# 👨‍💻 Author

**Raouf Yahiaoui**

Junior DevOps / Cloud Engineer in training.

Current focus:

* AWS
* Terraform
* Docker
* Kubernetes
* CI/CD
* Linux
* Cloud Infrastructure
