#!/bin/bash

# 遍历当前目录下的所有子目录, 并删除目录下的 build、resnet 文件和 codegen 目录
for dir in */ ; do
  # 检查是否是目录
  if [ -d "$dir" ]; then
    # 删除 build 目录（如果存在）
    [ -d "$dir/build" ] && echo "Deleting build directory in $dir" && rm -rf "$dir/build"

    # 删除 resnet 可执行文件（如果存在）
    [ -f "$dir/resnet" ] && echo "Deleting resnet executable in $dir" && rm -f "$dir/resnet"

    # 删除 codegen 目录（如果存在）
    [ -d "$dir/codegen" ] && echo "Deleting codegen directory in $dir" && rm -rf "$dir/codegen"
  fi
done

echo "Cleanup completed."