terraform {
  backend "s3" {
    bucket = "sensor-tf-aps"
    key    = "tf-state"
    region = "ap-south-1"
  }
}

module "sensor_ec2" {
  source = "./sensor_ec2"
}

module "sensor_model" {
  source = "./sensor_model_bucket"
}

module "sensor_ecr" {
  source = "./sensor_ecr"
}