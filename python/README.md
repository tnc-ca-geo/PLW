# Build and deploy Lambda package

## 1. Build deploy package

With docker domain running, run ```sh build_deploy_package.sh``` which will 
generate a package.zip that does **not** contain the local code.

## 2. Add local code to that package

Run ```sh update_package.sh``` in order to add the local code.

## 3. Move the deploy package to S3

```aws s3 cp package.zip s3://plwassets```

## 4. Import code from s3 to a lambda function
