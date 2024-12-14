# Deforestation in Africa using AI documentation!

## Description

Identification of deforestation in Africa using spatiotemporal GIS data.

## Commands

The Makefile contains the central entry points for common tasks related to this project.

### Syncing data to cloud storage

* `make sync_data_up` will use `az storage blob upload-batch -d` to recursively sync files in `data/` up to `msc-thesis-container/data/`.
* `make sync_data_down` will use `az storage blob upload-batch -d` to recursively sync files from `msc-thesis-container/data/` to `data/`.


