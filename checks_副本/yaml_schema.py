import yaml

def check_yaml_schema(yaml_path: str = "./hat_data.yaml"):
    """校验训练yaml结构、类别数量匹配安全帽2类"""
    required_keys = ["train","val","test","nc","names"]
    try:
        with open(yaml_path,"r",encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
    except Exception as e:
        return {"check":"yaml_schema","severity":"ERROR","msg":f"yaml读取失败:{str(e)}"}

    miss = [k for k in required_keys if k not in cfg]
    if miss:
        return {"check":"yaml_schema","severity":"ERROR","msg":f"缺失关键字:{miss}"}
    # 必须2个类别
    if cfg["nc"] !=2:
        return {"check":"yaml_schema","severity":"ERROR","msg":f"nc应为2，当前{cfg['nc']}"}
    if set(cfg["names"].values()) != {"hat","person"}:
        return {"check":"yaml_schema","severity":"WARNING","msg":"类别名称不匹配hat/person"}

    print("[YAML校验] 配置格式完全合规")
    return {"check":"yaml_schema","severity":"INFO","msg":"yaml校验通过"}

if __name__ == "__main__":
    # 关键修复：路径左右加上双引号
    check_yaml_schema(yaml_path="/Users/wenyan/Desktop/hat_data.yaml")