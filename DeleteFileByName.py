import os
import shutil

# 这个函数是用来递归遍历文件夹里面所有内容，包括文件夹和文件，将它们分开放到两个列表
# 顾名思义：file_list 是放文件的、dir_list 是放目录的
def get_file_path(root_path, file_list, dir_list):
	# 获取该目录下所有的文件名称和目录名称
	dir_or_files = os.listdir(root_path);
	for dir_file in dir_or_files:
		# 获取目录或者文件的路径
		dir_file_path = os.path.join(root_path, dir_file)
		# 判断该路径为文件还是路径
		if os.path.isdir(dir_file_path):
			dir_list.append(dir_file_path)
			# 递归获取所有文件和目录的路径
			get_file_path(dir_file_path, file_list, dir_list)
		else:
			file_list.append(dir_file_path);

# 这个函数是用来将遍历好的文件列表中里面某些需要删除的文件进行删除操作
# 如果你不放心带后缀的文件删除后有啥影响，在下面有一句注释的代码，是用来将源文件复制拷贝到某个目录里
def delete_file(file_list):
        # file_list 已经在上面的函数遍历完成 现在里面的内容是所有的文件
        # 我们挨个遍历 找到符合删除文件的条件
	for file_name in file_list:
                # 如果文件的后缀符合要求 就进行操作
		if file_name.endswith(").png"):
                        # 在屏幕上打印出来文件的名称 你得知道你删除了什么文件
			print(file_name)
			# 下面代码是将删除这个后缀的文件拷贝到一个备份的文件夹，其实就是多此一举
                        # 一开始是为了确认下删除了那个带后缀的文件会不会对源文件产生一些影响
			# shutil.copy(file_name.split(".baiduyun.p.downloading")[0], r"E:\BackUP")
                        # 直接进行删除
			os.remove(file_name)

if __name__ == "__main__":
	# 根目录路径
	root_path = r"C:/Users/jungle/AppData/Roaming/Typora/typora-user-images";
	# 用来存放所有的文件路径
	file_list = []
	# 用来存放所有的目录路径
	dir_list = []
	get_file_path(root_path, file_list, dir_list)
	# print(file_list)
	# print(dir_list)
	delete_file(file_list)
	os.system("pause")