provider "aws" {
  region = var.aws_region
}

# Base Network
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name = "archgen-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = true
  tags = {
    Name = "archgen-public-subnet"
  }
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
  tags = {
    Name = "archgen-private-subnet"
  }
}


# S3 Static Hosting / CloudFront
resource "aws_s3_bucket" "frontend_frontend1" {
  bucket = "archgen-frontend-frontend1"
}
resource "aws_s3_bucket_public_access_block" "frontend_frontend1_access" {
  bucket = aws_s3_bucket.frontend_frontend1.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}


# ECS Fargate Compute
resource "aws_ecs_cluster" "cluster_backend1" {
  name = "cluster-backend1"
}
resource "aws_ecs_task_definition" "task_backend1" {
  family                   = "task-backend1"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  container_definitions    = jsonencode([
    {
      name      = "api-container"
      image     = "nginx:latest"
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}
resource "aws_ecs_service" "service_backend1" {
  name            = "service-backend1"
  cluster         = aws_ecs_cluster.cluster_backend1.id
  task_definition = aws_ecs_task_definition.task_backend1.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets = [aws_subnet.private.id]
  }
}


# RDS PostgreSQL
resource "aws_db_instance" "db_db1" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "15.4"
  instance_class       = "db.t3.micro"
  username             = "adminuser"
  password             = var.db_password
  skip_final_snapshot  = true
  identifier           = "db-db1"
}

