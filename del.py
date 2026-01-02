import subprocess
import re

def generate_requirements():
    # 使用 pip freeze 生成原始 requirements.txt
    with open("requirements.txt", "w", encoding="utf-8") as f:
        subprocess.run(["pip", "freeze"], stdout=f)

def clean_requirements():
    cleaned = []
    with open("requirements.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # 去掉 ==、>=、<=、~=、@ file:// 等后缀，只保留包名
            pkg = re.split(r"==|>=|<=|~=|@ file://| @", line)[0].strip()
            if pkg:
                cleaned.append(pkg)

    # 写回文件
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned) + "\n")

if __name__ == "__main__":
    generate_requirements()
    clean_requirements()
    print("requirements.txt 已生成并清理版本号，只保留包名。")
