# terraform-path-hash

Terraform module for hashing the contents of a path. It looks at a file or directory and generates a sha256 hash based on the file names and contents. It ignores file times.

This is a helper module that can be used to force changes whenever files have changed. 

## Usage

For example, with API Gateway you might want to trigger deployments.

```hcl
module "path_hash" {
  source = "github.com/claranet/terraform-path-hash?ref=v0.1.0"
  path   = "${path.module}"
}

resource "aws_api_gateway_deployment" "api" {
  ...
  stage_description = "${module.path_hash.result}"
  ...
}
```
