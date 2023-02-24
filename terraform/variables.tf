variable "prefix" {
  description = "The prefix used for all resources in this environment"
  default = "module12-pdc-todo"
}

variable "OAUTH_CLIENT_ID" {
  sensitive = true
}

variable "OAUTH_CLIENT_SECRET" {
  sensitive = true
}
