sudo apt-get install python3-pip
sudo apt-get install liblapack-dev
sudo apt-get install libblas-dev

pip3 install --upgrade pip

pip3 install virtualenv
virtualenv fin

source fin/bin/activate
pip3 install pandas
pip3 install matplotlib
pip3 install cvxopt
pip3 install jupyter
pip3 install pandas_datareader

pip3 install --upgrade pandas
pip3 install --upgrade matplotlib
pip3 install --upgrade cvxopt
pip3 install --upgrade jupyter
pip3 install --upgrade pandas_datareader