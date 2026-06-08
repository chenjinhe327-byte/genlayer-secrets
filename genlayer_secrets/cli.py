from pathlib import Path
from shutil import copy

def main():
    """生成 weather 安全模板"""
    templates_dir = Path(__file__).parent / "templates"
    contracts_dir = Path("contracts")
    contracts_dir.mkdir(exist_ok=True)

    src = templates_dir / "weather.py"
    dst = contracts_dir / "weather_secure.py"

    if src.exists():
        copy(src, dst)
        print("🎉 成功生成安全模板！")
        print(f"   文件位置: {dst}")
        print("\n部署命令：")
        print("   genlayer deploy contracts/weather_secure.py")
    else:
        print("❌ 找不到模板文件")

if __name__ == "__main__":
    main()