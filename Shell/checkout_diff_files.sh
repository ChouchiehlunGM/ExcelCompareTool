#!/bin/bash
# This is our first script.
diff_file_name="diff_files"
unzip_dir_name="diff_files.zip_files"
result_file="result.txt"
xlsx_file="xlsx"
xls_file="xls"

# 输入前后需要对比的commitid
echo "please check if python module: 'xlrd' and 'numpy' is installed !!!"
echo "if displayed garbled data when printed chinese code in bash, you can reference blog: https://blog.csdn.net/u012145252/article/details/81775362"
echo -n "please enter compare commit id -> "
read first_commit_id

echo -n "please enter compared commit id -> "
read second_commit_id

if [ ! $first_commit_id ]; then
   echo "compare commit id is null"
   exit
fi

if [ ! $second_commit_id ]; then
   echo "compared commit id is null"
   exit
fi

# 列出差异文件清单 只限文件名（包含路径）
echo "diff files: "
git diff --name-only $first_commit_id..$second_commit_id

# 将差异文件和解压后的文件夹放到项目git根目录
cd ..

# check是不是有diff_files.zip_files文件夹和diff_files.zip文件
# 删除旧数据
if [ -f $diff_file_name.zip ]
then
  rm -rf $diff_file_name.zip
fi

if [ -d $unzip_dir_name ]
then
  rm -rf $unzip_dir_name
fi

if [ -f $result_file ]
then
  rm -rf $result_file
fi

# 将差异文件打包
git archive -o $diff_file_name.zip $first_commit_id $(git diff --name-only $first_commit_id..$second_commit_id)

# 获取差异文件路径
basepath=$(cd `dirname $0`; pwd)

# 解压到当前目录
python $basepath/Tools/unzip.py $diff_file_name.zip


getDir(){
  for file in $1/*
  do
  if test -f $file; then
     arr=(${arr[*]} $file)
  else
     getDir $file
  fi
  done
}

# echo $basepath/$unzip_dir_name
getDir $basepath/$unzip_dir_name
# echo ${arr[@]}

for element in "${arr[@]}";
do
  zip_path=$unzip_dir_name/
  new_path=${element//$zip_path/} # 在将差异文件路径中去除解压缩文件目录
  file_name=$(basename "$new_path")
  # 获取需要对比的原始文件
  git checkout $second_commit_id -- "Database/"$file_name
done

# 创建差异文件
echo "" > $result_file

# 往差异文件中写入 为什么不用shell直接刺写入？
# 用shell脚本直接写入，中文会出现乱码，所以用python脚本写入
python $basepath/Tools/write_file.py $result_file "差异文件总览： "

# 将差异文件总览写入result中
for element in "${arr[@]}";
do
  zip_path=$unzip_dir_name/
  new_path=${element//$zip_path/} # 在将差异文件路径中去除解压缩文件目录
  file_name=$(basename "$new_path")
  if [ -f $new_path ]; then # 查看项目中本来是否含有该文件
    echo "modified：  $file_name   "
    python $basepath/Tools/write_file.py $result_file "修改文件-> $file_name"
  else
    echo "add:  $file_name   "
    python $basepath/Tools/write_file.py $result_file "添加文件-> $file_name"
  fi
done

python $basepath/Tools/write_file.py $result_file ""
python $basepath/Tools/write_file.py $result_file "m 表示修改， + 表示添加，- 表示删除 "

# 过滤表格文件
for element in "${arr[@]}";
do
  zip_path=$unzip_dir_name/
  new_path=${element//$zip_path/} # 在将差异文件路径中去除解压缩文件目录
  file_name=$(basename "$new_path")
  if [ -f $new_path ]; then # 查看项目中本来是否含有该文件
    if [ "${element##*.}" == "$xlsx_file" -o "${element##*.}" = "$xls_file" ]; then
       python $basepath/Tools/excel_compare.py $new_path $element $basepath/$result_file
    fi
  fi
done