# Adbloq
## Abstract
Adbloq utilizes Berkeley Vision Learning Caffe (BVLC) in order to detect and identify website advertisements. BVLC is responsible for creating the image classifier to determine what is and what is not an advertisement. 

The convnet is demonstrated by use of a proxy server, but it could be placed anywhere in a network between the client and an ad-insertion server.

Specifically, we use Squid3 as a proxy server in conjunction with the ICAP protocol to host our convnet.

Squid3 has the capability to act as an ICAP Client, so we created an ICAP server that handled the classification of responses containing images. The server would forward images that failed classification, and send a transparent image of similar resolution if it was identified as an ad.

## Contributors
Stefan Francisco, Kevin Manan, Thomas Stubblebine, Nathan Sanders

Advisor: Prof. Robert Bruce
## Dependencies

The system was tested on an Ubuntu 14.04 distribution, using distro packages for squid3 and PyPI packages for PyICAP and Python-Magic.

### Squid3

```
sudo apt-get install squid3
```

### PyICAP

```
pip install pyicap
```

### Python Magic
```
pip install python-magic
```

## Caffe Installation
Verify GPU computing and CUDA compatibility of hardware.
```
lspci | grep -i nvidia
uname -m && cat /etc/*release
 gcc --version
```
Install protobuf, leveldb, snappy, opencv, hdf5, protobuf, and boost
```
sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler
```
Install blas
```
sudo apt-get install libatlas-base-dev
```
Other dependencies: gflags glog lmdb
```
sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev
```
Install CUDA
```
wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1404/x86_64/cuda-repo-ubuntu1404_6.5-14_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1404_6.5-14_amd64.deb
sudo apt-get update
sudo apt-get install cuda
```


Add the following to the .bashsrc in your home folder
```
export CUDA_HOME=/usr/local/cuda-7.5 
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64 
PATH=${CUDA_HOME}/bin:${PATH} 
export PATH 
```


Install Anaconda
```
wget http://09c8d0b2229f813c1b93-c95ac804525aac4b6dba79b00b39d1d3.r79.cf1.rackcdn.com/
Anaconda-2.1.0-Linux-x86_64.sh
bash Anaconda-2.1.0-Linux-x86.sh
```
NOTE: It will ask if you would like to change the path? Yes.

Install Caffe
```
git clone 'https://www.github.com/BVLC/caffe'
cd caffe
cp Makefile.config.example Makefile.config
make all -j8
make test -j8
make runtest -j8
```
## Creating a Database
#### Gathering Images
A python script is developed by Kevin Manan that automates the image mining process. Another  script was developed to recursively rename images in a format required by LMDB.
#### Creating an LMDB Database
Python script *create_lmdb.py* is used to do the following:
1. Equalization of all 3 color channels
2. Resizing to 224x224
3. Divide training data into two sets:
	- 5/6 of the images will be used for training.
	- The remaining 1/6 of the images will be used for validation.
4. Each of the images will have a label: 0 if it is a negative image, 1 if it is a positive image.
5. Store data into two databases: *train_lmdb* & *validation_lmdb*

NOTE: A mean image of all of the data ensures each feature pixel has 0 mean.

## Defining a Model
*model_1_train* defines the model of our image classifier. It has been developed under the foundation of Jeff Donahue's CaffeNet.

## Defining a Solver
The solver is responsible in the guidelines of the training and validation of our model. 

## Training the Model
We have developed two training models. One model is trained upon the database of a wide variety of advertisements. The other is focused on a more specific advertisement: insurance. 

#### Wide Variety Model
This model consists of 1200 positive images and 1800 negative images.

Validation Accuracy: 86%

#### Insurance Advertisement Model
This model consists of 400 positive images and 3300 negative images

Validation Accuracy: 80% 

#### Hypothesis
Although it seems the wide variety model is more accurate than the insurance advertisement model, there are a couple of factors that will affect the model's accuracy in real time:

1. The negative images in the wide variety model does not consist of any advertisements. The model is more tuned strictly whether it is an advertisement vs it is not an advertisement.
2. The insurance advertisement model is fine-tuned in a website advertisement genre. As a result, negative images contain advertisements that are unrelated to insurance. This will provide more data in long term, when adding additional genres to the model. 

Therefore, in real time, the insurance advertisement model is a more approachable idea in filtering advertisements due to it's specific range of real-time advertisement possibilities. 


## Configuring Squid

These lines refer to modifying the file /etc/squid3/squid.conf

First, define the network your clients will be connecting from.
```
acl sjsu src 130.65.0.0/16  # San Jose State University network
```

Allow proxy access to clients:
```
http_access allow sjsu
```

Enable Squid ICAP client:
```
icap_enable on
```

Register ICAP service:
```
icap_service adbloq respmod_precache icap://localhost:13440/example
```
In this instance, adbloq is the name of the service, internal to squid.
respmod_precache indicates that responses should be sent to the ICAP server before being cached.
The ICAP URI indicates the server:port of your ICAP server, example is the ICAP method.

Squid should begin heartbeating with your ICAP server shortly!
