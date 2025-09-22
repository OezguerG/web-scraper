import subprocess
import sys
from pathlib import Path


def run_spider():
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    output_path = data_dir / "movie_links.json"

    data_dir.mkdir(parents=True, exist_ok=True)

    # Chat-GPT 14 - 15
    if output_path.exists():
        output_path.unlink()
    
    print("Running Scrapy spider...")

    # Chat-GPT 15 - 21 (runs and waits for subprocess)
    result = subprocess.run(
        [sys.executable, "-m", "scrapy", "runspider", "scrapy_spider.py", "-o", str(output_path)],
        cwd=str(base_dir),
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Spider failed:")
        print(result.stderr)
        return False

    print("\nSpider finished successfully.\n")  
    print(f"Output path: {output_path} \n")
    
    return True
