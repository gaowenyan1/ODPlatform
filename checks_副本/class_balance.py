from pathlib import Path
from collections import defaultdict

WARN_RATIO =50
INFO_RATIO=10

def check_class_balance(data_root: str = "./data"):
    splits = ["train","val","test"]
    cls_cnt = defaultdict(int)
    for split in splits:
        label_dir = Path(data_root)/split/"annotations"
        for txt in label_dir.glob("*.txt"):
            with open(txt,"r",encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    cid = int(line.split()[0])
                    cls_cnt[cid] +=1
    counts = list(cls_cnt.values())
    if len(counts)<2:
        ratio =0
        severity="INFO"
    else:
        max_c = max(counts)
        min_c = min(counts)
        ratio = max_c/min_c if min_c>0 else 999
        if ratio >= WARN_RATIO:
            severity="WARNING"
        elif ratio >= INFO_RATIO:
            severity="INFO"
        else:
            severity="INFO"
    res = {
        "check":"class_balance",
        "class_count":dict(cls_cnt),
        "max_min_ratio":round(ratio,2),
        "severity":severity
    }
    print(f"【类别均衡】0(hat):{cls_cnt.get(0,0)} 1(person):{cls_cnt.get(1,0)} 比值:{ratio:.2f} 等级:{severity}")
    return res

if __name__ == "__main__":
    check_class_balance()