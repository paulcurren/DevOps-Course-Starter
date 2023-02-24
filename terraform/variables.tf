variable "prefix" {
  description = "The prefix used for all resources in this environment"
  default = "module12-pdc-todo"
}

variable "client_id" {
  sensitive = true
}

variable "client_secret" {
  sensitive = true
}
