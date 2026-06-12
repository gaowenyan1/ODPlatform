from pathlib import Path

def check_pair_existence(data_root: str = "./data"):
    """校验：有标签无图片、有图片无标签"""
    splits = ["train", "val", "test"]
    no_img_label = []
    no_label_img = []

    for split in splits:
        img_dir = Path(data_root) / split / "images"
        label_dir = Path(data_root) / split / "annotations"

        img_stems = {f.stem for f in img_dir.glob("*.jpg")}
        label_stems = {f.stem for f in label_dir.glob("*.txt")}

        orphan_labels = label_stems - img_stems
        empty_imgs = img_stems - label_stems

        no_img_label.extend([str(label_dir / f"{s}.txt") for s in orphan_labels])
        no_label_img.extend([str(img_dir / f"{s}.jpg") for s in empty_imgs])

    # 修复这里：整体加括号再调用glob
    total_labels = len([p for s in splits for p in (Path(data_root)/s/"annotations").glob("*.txt")])
    orphan_ratio = len(no_img_label) / total_labels if total_labels else 0

    result = {
        "check": "pair_existence",
        "orphan_label_count": len(no_img_label),
        "empty_image_count": len(no_label_img),
        "orphan_ratio": round(orphan_ratio,4),
        "severity": "WARNING" if orphan_ratio >=0.1 else "INFO",
        "orphan_files": no_img_label,
        "empty_img_files": no_label_img
    }
    print(f"【配对校验】孤儿标签{len(no_img_label)}个，无标注图片{len(no_label_img)}个，异常占比{orphan_ratio:.2%}")
    return result

if __name__ == "__main__":
    check_pair_existence()