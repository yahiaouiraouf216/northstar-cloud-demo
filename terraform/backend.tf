terraform {
  backend "s3" {
    bucket = "northstar-terraform-state-557629718261"
    key    = "northstar/terraform.tfstate"
    region = "us-east-1"
  }
}
