import os
import xml.etree.ElementTree as ET

IMG_DIR = "/Users/wenyan/Desktop/VOC2008/images"
XML_DIR = "/Users/wenyan/Desktop/VOC2008/annotations"
SAVE_LABEL_DIR = "/Users/wenyan/Desktop/VOC2008/labels"

# 类别映射 和你的 classes.txt 保持一致
CLASS_NAMES = ["hat", "person"]

# 创建标签文件夹（不存在则自动新建）
os.makedirs(SAVE_LABEL_DIR, exist_ok=True)


def convert_xml_to_yolo(xml_path, img_w, img_h):
    """单文件XML转YOLO格式"""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    yolo_lines = []

    # 遍历所有目标框
    for obj in root.iter("object"):
        # 获取标签名
        cls_name = obj.find("name").text.strip()
        if cls_name not in CLASS_NAMES:
            print(f"警告：发现未知标签 {cls_name}，跳过该目标")
            continue

        # 获取类别ID
        cls_id = CLASS_NAMES.index(cls_name)

        # 读取VOC坐标：xmin, ymin, xmax, ymax
        bndbox = obj.find("bndbox")
        xmin = float(bndbox.find("xmin").text)
        ymin = float(bndbox.find("ymin").text)
        xmax = float(bndbox.find("xmax").text)
        ymax = float(bndbox.find("ymax").text)

        # 转为YOLO归一化坐标 (中心x, 中心y, 宽, 高)
        x_center = (xmin + xmax) / 2.0 / img_w
        y_center = (ymin + ymax) / 2.0 / img_h
        box_w = (xmax - xmin) / img_w
        box_h = (ymax - ymin) / img_h

        # 拼接成一行文本
        line = f"{cls_id} {x_center:.6f} {y_center:.6f} {box_w:.6f} {box_h:.6f}"
        yolo_lines.append(line)

    return yolo_lines


if __name__ == "__main__":
    # 遍历所有xml文件
    xml_files = [f for f in os.listdir(XML_DIR) if f.endswith(".xml")]
    total = len(xml_files)
    print(f"共检测到 {total} 个XML标注文件，开始转换...")

    for idx, xml_file in enumerate(xml_files, 1):
        # 文件名（去掉后缀）
        file_stem = os.path.splitext(xml_file)[0]
        xml_full_path = os.path.join(XML_DIR, xml_file)
        img_full_path = os.path.join(IMG_DIR, f"{file_stem}.jpg")

        # 校验图片是否存在
        if not os.path.exists(img_full_path):
            print(f"跳过 {xml_file}：对应图片 {file_stem}.jpg 不存在")
            continue

        # 读取图片尺寸（从xml中直接取，不用额外读图片）
        tree = ET.parse(xml_full_path)
        root = tree.getroot()
        img_w = int(root.find("size/width").text)
        img_h = int(root.find("size/height").text)

        # 转换
        yolo_content = convert_xml_to_yolo(xml_full_path, img_w, img_h)

        # 写入txt标签
        txt_file = f"{file_stem}.txt"
        txt_full_path = os.path.join(SAVE_LABEL_DIR, txt_file)
        with open(txt_full_path, "w", encoding="utf-8") as f:
            f.write("\n".join(yolo_content))

        if idx % 100 == 0:
            print(f"已完成 {idx}/{total}")

    print("✅ 全部转换完成！")