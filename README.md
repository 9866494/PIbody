# Instalition

In repository root folder

All of the described process have been tested on Raspberry Pi3, with RASPBIAN JESSIE LITE (May 2016 Version)

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-rpi.gpio python-setuptools nodejs npm git
sudo easy_install pip
sudo pip install -r requirements.txt
cd static/
npm install
```

# Installing web camera dependencies

```
sudo apt-get install libjpeg8-dev imagemagick libv4l-dev subversion
cd ~
svn co https://svn.code.sf.net/p/mjpg-streamer/code/mjpg-streamer/ mjpg-streamer
cd mjpg-streamer
make mjpg_streamer input_file.so input_uvc.so output_http.so
sudo cp mjpg_streamer /usr/local/bin
sudo cp output_http.so input_file.so input_uvc.so /usr/local/lib/
sudo cp -R www /usr/local/www
export LD_LIBRARY_PATH=/usr/local/lib/
echo "export LD_LIBRARY_PATH=/usr/local/lib/" >> ~/.bashrc
```

# Running the video stream

The settings depends on your camera module, please read the official manuals

```
/usr/local/bin/mjpg_streamer -i "/usr/local/lib/input_uvc.so -d /dev/video0 -y -f 24" -o "/usr/local/lib/output_http.so -w /usr/local/www"
```

# Run

```
./server.py
```