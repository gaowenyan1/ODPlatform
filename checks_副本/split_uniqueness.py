from pathlib import Path

def check_split_uniqueness(data_root: str = "./data"):
    """校验train/val/test文件夹存在、样本数量合规"""
    splits = ["train", "val", "test"]
    split_cnt = {}
    err_msg = []
    severity = "INFO"

    for split in splits:
        img_dir = Path(data_root)/split/"images"
        cnt = len(list(img_dir.glob("*.jpg")))
        split_cnt[split] = cnt

    # 训练集为空=最高错误
    if split_cnt["train"] == 0:
        err_msg.append("train训练集为空，无法启动训练")
        severity = "ERROR"
    # 验证集为空警告
    if split_cnt["val"] == 0:
        err_msg.append("val验证集缺失")
        severity = "WARNING"
    # val/test少于30条提示
    if 0 < split_cnt["val"] <30:
        err_msg.append(f"val样本仅{split_cnt['val']}，少于30")
    if 0 < split_cnt["test"] <30:
        err_msg.append(f"test样本仅{split_cnt['test']}，少于30")

    res = {
        "check":"split_uniqueness",
        "sample_count":split_cnt,
        "error_msg":err_msg,
        "severity":severity
    }
    print(f"【划分校验】train:{split_cnt['train']} val:{split_cnt['val']} test:{split_cnt['test']} 等级:{severity}")
    return res

if __name__ == "__main__":
    check_split_uniqueness()