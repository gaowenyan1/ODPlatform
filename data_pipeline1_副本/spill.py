import os
import random
import shutil

# ===================== 1. 你的原始文件路径（无需修改，直接运行） =====================
# 原始图片文件夹
SRC_IMG = "/Users/wenyan/Desktop/VOC2008/images"
# 原始txt标签文件夹（你命名为 annotations）
SRC_LABEL = "/Users/wenyan/Desktop/VOC2008/annotations"

# ===================== 2. 拆分后存放的目标总文件夹 =====================
DST_ROOT = "/Users/wenyan/Desktop/hat_datasets"

# 拼接分层子目录
img_train = os.path.join(DST_ROOT, "images", "train")
img_val = os.path.join(DST_ROOT, "images", "val")
img_test = os.path.join(DST_ROOT, "images", "test")

label_train = os.path.join(DST_ROOT, "annotations", "train")
label_val = os.path.join(DST_ROOT, "annotations", "val")
label_test = os.path.join(DST_ROOT, "annotations", "test")

# 创建所有文件夹（不存在则自动新建）
for folder in [img_train, img_val, img_test, label_train, label_val, label_test]:
    os.makedirs(folder, exist_ok=True)

# 获取所有jpg图片，并打乱顺序
img_files = [f for f in os.listdir(SRC_IMG) if f.lower().endswith(".jpg")]
random.shuffle(img_files)
total_num = len(img_files)

# 按 8:1:1 计算数量
train_count = int(total_num * 0.8)
val_count = int(total_num * 0.1)

# 划分三组文件列表
train_files = img_files[:train_count]
val_files = img_files[train_count: train_count + val_count]
test_files = img_files[train_count + val_count:]

# 定义复制函数：图片 + 对应txt标签一起复制
def copy_group(file_list, target_img, target_label):
    for img_name in file_list:
        # 复制图片
        shutil.copy(os.path.join(SRC_IMG, img_name), os.path.join(target_img, img_name))
        # 替换后缀，找到对应txt标签
        txt_name = os.path.splitext(img_name)[0] + ".txt"
        src_txt_path = os.path.join(SRC_LABEL, txt_name)
        # 标签存在才复制
        if os.path.exists(src_txt_path):
            shutil.copy(src_txt_path, os.path.join(target_label, txt_name))

# 执行复制
copy_group(train_files, img_train, label_train)
copy_group(val_files, img_val, label_val)
copy_group(test_files, img_test, label_test)

# 打印结果
print("✅ 数据集拆分完成！")
print(f"总数据量：{total_num} 张")
print(f"训练集：{len(train_files)} 张")
print(f"验证集：{len(val_files)} 张")
print(f"测试集：{len(test_files)} 张")