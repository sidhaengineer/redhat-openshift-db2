FROM python:3.11.4
# add python in our docker container

RUN mkdir /appfolder
# make folder in docker container #linux

COPY . /appfolder
# copy all files of this folder to out docker folder

RUN python -m pip install -r /appfolder/requirements.txt
# install required module which is in requirement.txt file to container

EXPOSE 5000
# run on 5000 port

CMD [ "python", "/appfolder/app.py" ]
# execute application in container
# C:\Users\91990\Desktop\THIS IS IT>docker build -t jobboard:1.0 .
# >docker images
# >docker run -p 5000:5000 jobboard:1.0       # docker port:laptop port
# >docker rmi jobboard:1.0   # to remove applicatoion
# View summary of image vulnerabilities and recommendations → docker scout quickview
# Learn more about vulnerabilities → docker scout cves jobboard
# >docker ps : information about containers
# >docker login 
# docker tag jobboard:1.0 sidhaengineer/jobboard:1.0    # creates copy of image with username/projectname so it can be pushed to docker repositary