# SILA

Simple Image Labeling Application

SILA is a web application for labeling image data sets.

# Running locally

1. Build the docker image

```
> docker build . -t bd5ton_sila
```
2. Run SILA as docker container

# Environment variables

## MODERATE_SOURCE_DIR
Images for Moderate phase are read from this directory. You can volume map a directory in your host to this location inside the SILA container.

## MODERATE_SINK_DIR
Output of Moderate phase are dumped in this directory.

## MODERATE_REJECTED_DIR
Images rejected during Moderate phase are moved to this directory.


# Future plan
- Labeling jobs should be organized in projects
- Each project should be comprised of one or more phases
- Moderate phase
- Text detection phase
- Cropping phase
- Export as a .zip file
- Export to AWS S3
- Export to Google Cloud Storage