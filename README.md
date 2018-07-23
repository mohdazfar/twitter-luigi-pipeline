This data pipleine is written to analyze data based on certain related keywords. For the sake of example, I have used Twitter data specific to Genereal Elections 2018 in Pakistan but the pipeline can be used for any set of related keywords. Data is extracted from Twitter, cleaned, dumped to database and then analysed in the whole pipeline. The pipeline can be run easily by following the below steps:

**Steps**
1. Clone the repository.
2. Install Docker.
3. Run the docker-compose.yml to build our image.
```sh
$ docker-compose up
```
4. Copy the repository folder to our docker image. The reason for copying to ./app is because we created the working directory in our image to be ./app
```sh 
$ docker cp /REPO_FOLDER IMAGE_NAME:./app/REPO_FOLDER
```
5. Open mongodb in the container and create database named `luigipieline`. If you want to change the db name then you need to change it in `mongo_dump.py`. 
```sh
:/app# mongo
> use luigipipeline
switched to db luigipipeline
> db.createCollection("twitter")
{ 'ok' : 1 }
```
6. Now you are ready to run the pipeline inside the container. The following command will run the main pipeline script `luigi_pipeline.py`. The main process to run is `DataAnalysis` class but first all the dependent processes will be run. 
```sh
:/app# python luigi_pipeline.py --workers 3 DataAnalysis --localscheduler
```

**Good Luck!**
