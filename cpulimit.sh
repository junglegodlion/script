#!/bin/bash
# auth:kaliarch
# func:sys info check
# version:v1.0
# sys:centos6.x/7.x

# 在"set -e"之后出现的代码，一旦出现了返回值非零，整个脚本就会立即退出。
# id -u （显示当前用户的uid）
#  -gt 大于
# exit 1 代表非正常运行导致退出程序
# &&左边的命令（命令1）返回真(即返回0，成功被执行）后，&&右边的命令（命令2）才能够被执行
set -e
[ $(id -u) -gt 0 ] && exit 1

# cpu使用超过百分之多少进行限制
PEC_CPU=80

# 限制进程使用百分之多少,如果程序为多线程，单个cpu限制为85，如果为多核心，就需要按照比例写，例如cpu为2c，像限制多线程占比80%，就写170
LIMIT_CPU=85
# 日志
LOG_DIR=/var/log/cpulimit/

# 超过阀值进程pid
PIDARG=$(ps -aux |awk -v CPU=${PEC_CPU} '{if($3 > CPU) print $2}')
CPULIMITCMD=$(which cpulimit)

install_cpulimit() {
	[ ! -d /tmp ] && mkdir /tmp || cd /tmp
	wget -c https://github.com/opsengine/cpulimit/archive/v0.2.tar.gz
	tar -zxf v0.2.tar.gz
	cd cpulimit-0.2 && make
	[ $? -eq 0 ] && cp src/cpulimit /usr/bin/
}


do_cpulimit() {
[ ! -d ${LOG_DIR} ] && mkdir -p ${LOG_DIR}
for i in ${PIDARG};
# awk中，$2：表示第二个字段
# print $0 就是打印整行内容
do
        MSG=$(ps -aux |awk -v pid=$i '{if($2 == pid) print $0}')
        echo ${MSG}
	[ ! -d /tmp ] && mkdir /tmp || cd /tmp
	nohup ${CPULIMITCMD} -p $i -l ${LIMIT_CPU} &
        echo "$(date) -- ${MSG}" >> ${LOG_DIR}$(date +%F).log
done
}

main() {
	# hash表的作用：大大提高命令的调用速率。
	# 判断cpulimit是否安装
	hash cpulimit 
	# 程序退出后, 用户可以 echo $? 来查看是 0 还是 1
	# $? 是一个特殊变量，用来获取上一个命令的退出状态，或者上一个函数的返回值。
	# 大部分命令执行成功会返回 0，失败返回 1
	# 判断cpulimit是否安装
	if [ $? -eq 0 ];then
		do_cpulimit
	else
		install_cpulimit && do_cpulimit
	fi			
}

main