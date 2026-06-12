from pathlib import Path

TOL = 1e-6
MIN_AREA = 1e-4
MAX_AR = 10.0

def check_label_format(data_root: str = "./data"):
    """校验YOLO标签数值、坐标越界、零面积/畸形宽高比框"""
    splits = ["train", "val", "test"]
    out_bound_files = []
    bad_box_files = []

    for split in splits:
        label_dir = Path(data_root) / split / "annotations"
        for txt in label_dir.glob("*.txt"):
            with open(txt,"r",encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip()]
            for line in lines:
                parts = line.split()
                # 格式位数校验
                if len(parts)!=5:
                    bad_box_files.append(str(txt))
                    break
                try:
                    cls, cx, cy, bw, bh = map(float, parts)
                except ValueError:
                    bad_box_files.append(str(txt))
                    break
                # 类别只能0/1
                if cls not in (0,1):
                    bad_box_files.append(str(txt))
                    break
                # 坐标越界判断
                x1 = cx - bw/2
                x2 = cx + bw/2
                y1 = cy - bh/2
                y2 = cy + bh/2
                if x1 < -TOL or x2 > 1+TOL or y1 < -TOL or y2 >1+TOL:
                    out_bound_files.append(str(txt))
                    break
                # 退化框、极端比例
                area = bw * bh
                ar = max(bw,bh)/min(bw,bh) if min(bw,bh)>0 else 0
                if area < MIN_AREA or ar > MAX_AR or bw<=0 or bh<=0:
                    bad_box_files.append(str(txt))
                    break

    # 修复：整体路径套括号再调用glob
    total_txt = sum(1 for s in splits for _ in (Path(data_root)/s/"annotations").glob("*.txt"))
    out_ratio = len(out_bound_files)/total_txt if total_txt else 0
    severity = "ERROR" if out_ratio >=0.1 else "WARNING"

    res = {
        "check":"label_format",
        "out_of_bound_count":len(out_bound_files),
        "invalid_box_count":len(bad_box_files),
        "out_bound_ratio":round(out_ratio,4),
        "severity":severity,
        "out_files":out_bound_files,
        "bad_box_files":bad_box_files
    }
    print(f"【标签格式】越界框文件{len(out_bound_files)}，无效框文件{len(bad_box_files)} 等级:{severity}")
    return res

if __name__ == "__main__":
    check_label_format()