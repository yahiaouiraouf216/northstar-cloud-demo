output "public_ip" {
  value = aws_instance.main.public_ip
}

output "public_dns" {
  value = aws_instance.main.public_dns
}

output "ec2_instance_id" {
  value = aws_instance.main.id
}