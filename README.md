# Volleyball-simulation-platform-based-on-quadrotor-UAV 
<h1/>仿真环境搭建</h1>
<h2/>1.	Ros kinetic 安装</h2>
$ sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'<br>
$ sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116<br>
$ sudo apt-get update<br>
$ sudo apt-get install ros-kinetic-desktop-full<br>
$ sudo rosdep init<br>
$ rosdep update<br>
$ echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc<br>
$ source ~/.bashrc<br>
$ sudo apt-get install python-rosinstall python-rosinstall-generator python-wstool build-essential<br>
终端输入roscore(若出现 started core service [/rosout] 则说明安装成功)<br>
安装网址：<herf/>http://wiki.ros.org/kinetic/Installation/Ubuntu</herf>
<h2/>2.	创建ros工作空间</h2>
$ mkdir -p ~/catkin_ws/src<br>
$ cd ~/catkin_ws<br>
$ catkin_make  （编译）<br>
$ source devel/setup.bash<br>
<h2/>3.ardrone 驱动程序安装</h2>
$ cd ~/catkin_ws/src<br>
$ git clone https://github.com/AutonomyLab/ardrone_autonomy.git -b SDK2<br>
$ catkin_make  （编译）<br>
$ source devel/setup.bash<br>
<h2/>4.	ardrone_simulator仿真环境包安装</h2>
$ cd ~/catkin_ws/src<br>
$ git clone https://github.com/iolyp/ardrone_simulator_gazebo7<br>
$ catkin_make  （编译）<br>
$ source devel/setup.bash<br>
<h2/>5.	启动仿真环境</h2>
$ cd ~/catkin_ws<br>
$ source devel/setup.bash<br>
$ roslaunch cvg_sim_gazebo ardrone_testworld.launch<br>
注意：若3、4中出现编译错误，即不能完成编译的情况下，运行以下代码：<br>
$ sudo apt-get install ros-kinetic-ardrone-autonomy<br>
<h1/>排球仿真竞技平台搭建</h1>
1.put the volleyball_fira/models to your folder home/.gazebo,put volleyball_fira/ardrone_volley to your workspace<br>
2.update the related model file volleyball_fira/ardrone_volley/models(some model I just use the absolute path ,so you should update it to your own path) <br>
3.run roslaunch ardrone_volley ardrone_volleyball.launch<br>
4.run python Game.py to start up <br>
5.run teamA.py to ready<br>
