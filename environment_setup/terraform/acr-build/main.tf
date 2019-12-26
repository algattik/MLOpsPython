data "archive_file" "source_dir" {
  type        = "zip"
  source_dir = var.source_dir
  output_path = "source_dir.tmp"
}

resource "null_resource" "acr-build" {
  triggers = {
    src_hash = data.archive_file.source_dir.output_sha
    registry = var.registry
    image = var.image
  }
  provisioner "local-exec" {
        working_dir = var.source_dir
        command = <<BASH
az acr build -r "${var.registry}" -t "${var.image}" .
BASH
    }
}
