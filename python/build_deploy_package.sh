docker run --name lambda -itd remotepixel/amazonlinux-gdal:2.4.2 /bin/bash
docker exec -it lambda bash -c 'pip3 install rasterio[s3] --no-binary numpy,rasterio -t /tmp/python -U'
docker exec -it lambda bash -c 'pip3 install fiona -t /tmp/python -U'
docker exec -it lambda bash -c 'pip3 install shapely -t /tmp/python -U'
docker exec -it lambda bash -c 'pip3 install pyproj -t /tmp/python -U'
docker exec -it lambda bash -c 'cd /tmp/python; zip -r9q /tmp/package.zip *'
docker exec -it lambda bash -c 'cd /var/task; zip -r9q --symlinks /tmp/package.zip lib/*.so*'
docker exec -it lambda bash -c 'cd /var/task; zip -r9q --symlinks /tmp/package.zip lib64/*.so*' # This step is not needed for `-light` image
docker exec -it lambda bash -c 'cd /var/task; zip -r9q /tmp/package.zip share'
docker cp lambda:/tmp/package.zip package.zip
docker stop lambda
docker rm lambda
