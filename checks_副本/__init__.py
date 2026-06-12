from .pair_exsistence import check_pair_existence
from .split_uniqueness import check_split_uniqueness
from .label_format import check_label_format
from .yaml_schema import check_yaml_schema
from .class_balance import check_class_balance

def run_all_checks(data_root, yaml_path):
    print("========== 开始全量数据质检 ==========\n")
    r1 = check_pair_existence(data_root)
    r2 = check_split_uniqueness(data_root)
    r3 = check_label_format(data_root)
    r4 = check_yaml_schema(yaml_path)
    r5 = check_class_balance(data_root)
    print("\n========== 全部质检结束 ==========")
    return [r1,r2,r3,r4,r5]

__all__ = [
    "check_pair_existence",
    "check_split_uniqueness",
    "check_label_format",
    "check_yaml_schema",
    "check_class_balance",
    "run_all_checks"
]