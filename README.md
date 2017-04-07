

<h3>Installation</h3>
1. Verify GPU computing and CUDA compatibility of hardware 




2. Install protobuf, leveldb, snappy, opencv, hdf5, protobuf, and boost

sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler
sudo apt-get install --no-install-recommends libboost-all-dev

3. Install blas

sudo apt-get install libatlas-base-dev

4. Other dependencies gflags glog lmdb

sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev

5. Install CUDA

wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1404/x86_64/cuda-repo-ubuntu1404_6.5-14_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1404_6.5-14_amd64.deb
sudo apt-get update
sudo apt-get install cuda

6. Add the following to the .bashsrc file in your home folder

export CUDA_HOME=/usr/local/cuda-7.5 
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64 
 
PATH=${CUDA_HOME}/bin:${PATH} 
export PATH 

7.Install Anaconda

wget http://09c8d0b2229f813c1b93-c95ac804525aac4b6dba79b00b39d1d3.r79.cf1.rackcdn.com/Anaconda-2.1.0-Linux-x86_64.sh
bash Anaconda-2.1.0-Linux-x86.sh
It will ask do you want to change the path? Say yes

8. Install caffe
git clone 'https://www.github.com/BVLC/caffe'
cd caffe
cp Makefile.config.example Makefile.config
make all -j8
make test -j8
make runtest -j8
