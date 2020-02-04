# add the code to the package
zip package.zip fire_risk.py
# move package to S3
aws s3 cp package.zip s3://plwassets
# deploy to lambda
aws lambda update-function-code --function-name fireRisk --s3-bucket plwassets --s3-key package.zip
