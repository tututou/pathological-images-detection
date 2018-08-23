# pathological-images-detection
pathological images detection


openslide-python installation:

    sudo apt-get install python3-openslide
    pip install openslide-python
    1. sudo apt-get install libopenjpeg-dev libsqlite3-dev 
    2. sudo apt-get install openslide-tools 
    3. sudo apt-get install python-openslide 
    4. sudo apt-get install python3-openslide
    https://www.linuxidc.com/Linux/2017-09/147187.htm
    https://github.com/uclouvain/openjpeg/blob/master/INSTALL.md
    https://www.cnblogs.com/yszr/p/8120475.html
    5. sudo apt install libtiff5=4.0.6-1

  
pyvips installation:

    Building libvips from a source tarball
    If the packaged version is too old, you might need to build from source.

    Download vips-x.y.z.tar.gz from the Download area(https://github.com/jcupitt/libvips/releases), then:

    $ tar xf vips-x.y.z.tar.gz
    $ cd vips-x.y.z
    $ ./configure
    Check the summary at the end of configure carefully. libvips must have build-essential, pkg-config, glib2.0-dev,             libexpat1-dev.

    You’ll need the dev packages for the file format support you want. For basic jpeg and tiff support, you’ll need libtiff5-     dev, libjpeg-turbo8-dev, and libgsf-1-dev. See the Dependencies section below for a full list of the things that libvips     can be configured to use.

    Once configure is looking OK, compile and install with the usual:

    $ make
    $ sudo make install
    $ sudo ldconfig
    By default this will install files to /usr/local.

    We have detailed guides on the wiki for building for Windows(https://github.com/jcupitt/libvips/wiki/Build-for-Windows)       and building for macOS(https://github.com/jcupitt/libvips/wiki/Build-for-macOS).
  
  
opencv-python installation:

    pip install opencv-python
  
