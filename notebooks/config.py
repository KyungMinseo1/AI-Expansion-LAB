import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)

# --- Paths ---
# 프로젝트의 루트 디렉토리
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 데이터 및 모델 경로
DATA_DIR = os.path.join(PROJECT_ROOT, '관련데이터')