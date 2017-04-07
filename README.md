# Adbloq
## Abstract
Adbloq utilizes Berkeley Vision Learning Caffe (BVLC) in order to detect and identify website advertisements. BVLC is responsible for creating the image classifier to determine what is and what is not an advertisement. 
## Contributors
Stefan Francisco, Kevin Manan, Thomas Stubblebine, Nathan Sanders

Advisor: Prof. Robert Bruce
## Dependencies

## Installation
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
#### Creating an LMDB Database
