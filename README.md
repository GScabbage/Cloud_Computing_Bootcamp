# Cloud_Computing_Bootcamp
## AWS Background
### AWS Global Infrastructure
#### AWS Regions
#### AWS Availability Zones
#### Advantages of Cloud Computing

### Public Cloud, Private Cloud and Hybrid Cloud Use Cases
- Infrastructure As Service (Iaas)
- Platform As Service (Paas)
- Software As Service (Saas)
- Cloud Data Centers

## AWS Services
- Elastic Compute Service `EC2`
- Simple Storage Service `S3`
- Virtual Private Network `VPC`
- Internet Gateway `IG`
- Route Tables `RT`
- Subnet `sn`
- Network Access Control `NACL`
- Security Groups `SG`
- Cloudwatch `CW`
- Simple Notification Service `SNS`
- Simple Queue Service `SQS`
- Load Balancers `LB` - `ALB` - `ELB` - `NLB`
- Autoscaling Groups `ASG`
- Amazon Machine Image `AMI`
- DynamoDB - MongoDB

## EC2
### Setting Up An EC2 Instance
- First Choose the `AMI` you would like for you instance, this will be the OS that it runs on. In this case it will be ubuntu 16.04
- Next choose the instance type, this is dependent on how much memory, storage, network capacity and cpus that you require. Generally the default option is fine
- Most storage is EBS only, which is Elastic Block Storage but some use SSDs.
- Next is configuring your instance details

### After Launching the Instance
- Connect to the instance via SSH on port 22
- If you are having problems connecting here is some debugging code that might help
```
eval ssh-agent

ssh-add "keyfile.pem"
```
- Update and upgrade system
- Install nginx with `sudo apt install nginx -y`
- nginx restart and enable
```
sudo systemctl restart nginx
sudo systemctl enable nginx
```
- check the public ip to ensure nginx is running on your browser
- install node correct version, which for this is an version 6.x
```
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install python-software-properties
sudo apt-get install -y nodejs
```
- install pm2 for this version of node using `sudo npm install pm2@^3 -g`
- it may not work in which case npm module is not installed, in which case run `sudo apt install npm -y`
- `app code` currently available on `localhost`, so need to be copied to the db
- you can clone a github repo with everything directly onto the machine or use the secure copy command `scp`
- I used scp with `scp -i keyfile.pem -r path/file or directory user@ipaddressofinstance:destinationlocation`
- for scp you might think to use root for the user but in the case of ubuntu, use ubuntu in its place to go in as a root user
- now once you have copied the app code accross, the nginx needs to be configured
- this can be done through scp the configuration file across or writing it into the ssh terminal
- for scp use the same command then either link the file or delete the original and replace it
- for linking use `sudo ln -s path/default /etc/nginx/sites-available/default`
- for replacing do
```
sudo rm /etc/nginx/sites-available/default
sudo cp path/default /etc/nginx/sites-available
```
- the restart and enable nginx again, with the commands used earlier
- then navigate back to your app folder then run `npm install` to get the node modules
- finally `npm start` to start the app and connect on your web browser to check it is working

#### Setting up a db instance
- Follow the steps given for setting up the instance for the app
- Except for the security group do not allow ports 80 and 3000 as they do nothing the db requires
- Instead open port 27017 for the public ip from your app instance
#### Configuring the db
- ssh into the db using the same method as before but change the ip
- first get the key and correct version of MongoDB
```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv D68FA50FEA312927
echo "deb https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
```
- then run the update and upgrade commands as used earlier
- install the version of mongodb required for the app with
```
sudo apt-get install -y mongodb-org=3.2.20 mongodb-org-server=3.2.20 mongodb-org-shell=3.2.20 mongodb-org-mongos=3.2.20 mongodb-org-tools=3.2.20
```
- then restart and enable MongoDB
```
sudo systemctl restart mongod
sudo systemctl enable mongod
```
- then similar to in the app instance, you can scp across the `mongod.conf` file and replace or link the file or just edit the `mongod.conf` already present
- editing it the easier option just `cd /etc` then `sudo nano mangod.conf`, all you need to change is the line with `127.0.0.1` to either `0.0.0.0` or the ip address of your app instance
- then restart and enable MongoDB again as was done earlier
#### Connecting the app to the DB
- ssh back into your app instance
- in order to for the app to connect to the db, you need to set up the environment variable
- this can be done manually everytime which is inconvenient or my running a couple of lines of code that add it permanently
```
sudo echo 'export DB_HOST="mongodb://ipofdb:27017/posts"' >> .bashrc
source ~/.bashrc
```
- then the database needs to be seeded using `path/seed.js`
- now you can start the app up again and it will connect to the db

## Replications through AMIs
- from any instance you can creature a duplicate machine image called an `AMI`
- this allows you to easily replicate a preconfigured instance and allows you to return to an earlier point if something goes wrong
- basically the save game of AWS
- to do it, select the instance you want to make an AMI from and go to actions
- then got to images and templates then select create image
- you can give it a name, and change a few setting then you can create your image
- any programs currently running on your instance when it is made into an AMI will also be running when you start your new instance with your AMI

## Monitoring
### 4 Golden Signals
- Latency: Time to complete request
- Traffic: Measure of Demand
- Errors: Services Failing
- Saturation: How Full is the service

### Automation of Monitoring Response
- Application Load Balancer (ALB)
- Autoscaling Group
- Launch Template Config - how many instances at all times
- 2 instances - min=2 max=3
- Policies of scaling out and scaling in to minimum

#### Scaling on Demand
- Scaling up vs Scaling out
- Scaling up - increases the size of your instance
- Scaling Out - increases the number of instances
