<h1><p align="center">Adbloq</p></h1>
<h2>Abstract</h2>
Adbloq utilizes Berkeley Vision Learning Caffe (BVLC) in order to detect and identify website advertisements. BVLC is responsible for creating the image classifier to determine what is and what is not an advertisement. 

<h2>Contributors</h2>
Stefan Francisco, Kevin Manan, Nathan Sanders, Thomas Stubblebine
<br>
With advice from Professor Robert Bruce 

<h2>Dependencies</h2>

<h2>Installation</h2>
<h4>1. Verify GPU computing and CUDA compatibility of hardware </h4>

<i>
lspci | grep -i nvidia
<br>
uname -m && cat /etc/*release
<br>
 gcc --version
 </i> 



<h4>2. Install protobuf, leveldb, snappy, opencv, hdf5, protobuf, and boost</h4>
<i>
sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler
<br>
sudo apt-get install --no-install-recommends libboost-all-dev
</i>

<h4>3. Install blas</h4>
<i>
sudo apt-get install libatlas-base-dev
</i>
<h4>4. Other dependencies gflags glog lmdb</h4>
<i>
sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev
</i>
<h4>5. Install CUDA</h4>
<i>
wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1404/x86_64/cuda-repo-ubuntu1404_6.5-14_amd64.deb
<br>
sudo dpkg -i cuda-repo-ubuntu1404_6.5-14_amd64.deb
<br>
sudo apt-get update
<br>
sudo apt-get install cuda
</i>
<h4>6. Add the following to the .bashsrc file in your home folder</h4>
<i>
export CUDA_HOME=/usr/local/cuda-7.5 
<br>
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64 
 
PATH=${CUDA_HOME}/bin:${PATH} 
<br>
export PATH 
</i>
<h4>7.Install Anaconda</h4>
<i>
wget http://09c8d0b2229f813c1b93-c95ac804525aac4b6dba79b00b39d1d3.r79.cf1.rackcdn.com/
<br>
Anaconda-2.1.0-Linux-x86_64.sh
<br>
bash Anaconda-2.1.0-Linux-x86.sh
<br>
It will ask do you want to change the path? Say yes
</i>
<h4>8. Install caffe</h4>
<i>
git clone 'https://www.github.com/BVLC/caffe'
<br>
cd caffe
<br>
cp Makefile.config.example Makefile.config
<br>
make all -j8
<br>
make test -j8
<br>
make runtest -j8
</i>
<h4>Creating Database</h4>
<u>Gathering Images</u>
A python script is developed by Kevin Manan that automates the image mining process. Another  script was developed to recursively rename images in a format required by LMDB.
<u>Creating an LMDB database</u>
Python script <i>create_lmdb.py</i> is used to do the following:
<br>
1. Equalization of all 3 color channels
2. Resizing to 224x224
3. Divide training data into two sets:
	- 5/6 of the images will be used for training.
	- The remaining 1/6 of the images will be used for validation.
4. Each of the images will have a label: 0 if it is a negative image, 1 if it is a positive image.
5. Store data into two databases: <i>train_lmdb</i> & <i>validation_lmdb</i>
<br>
A mean image of all of the data ensures each feature pixel has 0 mean.