# 예측 모델 기반 가로 쓰레기통 고위험군 분석 및 인프라 개선방안 탐구
(Exploration of Prediction-based High-risk Areas for Street Trash Cans and Infrastructure Improvement)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![GeoPandas](https://img.shields.io/badge/GeoPandas-1.1.2-green.svg)](https://geopandas.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📌 Overview
이 프로젝트는 서울시(특히 마포구)의 유동인구 데이터와 도시 환경 요인을 분석하여, 가로 쓰레기통 설치가 시급한 **고위험군 지역**을 예측하고 최적의 인프라 개선 방안을 제안하는 것을 목표로 합니다.

주요 연구 및 개발 내용:
- 서울시 공공 데이터 및 생활인구/유동인구 데이터 전처리
- XGBoost 및 LightGBM 모델을 이용한 유동인구 밀도 및 쓰레기 배출 위험도 예측
- 공간 분석(Geospatial Analysis)을 통한 가로 쓰레기통 최적 입지 선정 및 시각화

---

## 🖼️ Visualizations

### 1. 모델 예측 유동인구 밀도 & 가로 쓰레기통 위치 시각화
모델이 예측한 유동인구 밀도와 현재 마포구 내 가로 쓰레기통의 위치를 중첩하여 나타낸 결과입니다. 유동인구가 밀집된 지역에 쓰레기통 인프라가 적절히 배치되어 있는지 확인합니다.

![모델 예측 유동인구 밀도 & 가로 쓰레기통 위치 시각화](visualization/모델%20예측%20유동인구%20밀도%20&%20가로%20쓰레기통%20위치%20시각화_2.png)

### 2. 실제 유동인구 밀도 & 가로 쓰레기통 위치 시각화
실제 관측된 유동인구 밀도 데이터를 기반으로 한 시각화 자료입니다.

![유동인구 밀도 & 가로 쓰레기통 위치 시각화](visualization/유동인구%20밀도%20&%20가로%20쓰레기통%20위치%20시각화_2.png)

---

## 📂 Project Structure
```text
.
├── models/              # 학습된 모델 파일 (.pkl, .model 등)
├── notebooks/           # Jupyter Notebooks (전처리, 학습, 시각화)
│   ├── config.py        # 프로젝트 경로 및 환경 변수 설정
│   ├── utils.py         # 데이터 처리 유틸리티 클래스/함수
│   ├── data.ipynb       # 공공 데이터 통합 및 전처리
│   ├── data_for_seoul.ipynb  # 서울시 전체 데이터 처리
│   ├── data_for_mapo.ipynb   # 마포구 타겟 데이터 상세 처리
│   ├── train.ipynb      # ML 모델(XGBoost, LGBM) 학습 및 검증
│   └── result_visualization.ipynb # 최종 결과물 시각화
├── preprocessed_data/   # 정제된 데이터셋 (CSV, GeoJSON 등)
├── visualization/       # 생성된 시각화 이미지 (.png)
├── 관련데이터/          # 서울시 상권, 쓰레기통, 지오코딩 등 원천 데이터
├── 관련논문/            # 분석에 참고한 관련 연구 문헌
├── 발표자료/            # 프로젝트 발표 PPT 및 관련 문서
├── requirements.txt     # 파이썬 의존성 패키지 목록
└── README.md            # 프로젝트 개요 및 안내
```

---

## 🛠️ Requirements & Setup

### 1. Requirements
- Python 3.8+
- 주요 라이브러리:
  - `geopandas`, `pandas`, `numpy`, `shapely`, `pyproj`
  - `xgboost`, `lightgbm`, `scikit-learn`
  - `matplotlib`, `jupyter`

### 2. Installation
```bash
git clone <repository-url>
cd AI-Expansion-LAB
pip install -r requirements.txt
```

### 3. Environment Variables
`.env` 파일을 프로젝트 루트에 생성하고 필요한 경로를 설정할 수 있습니다 (기본값은 `notebooks/config.py` 참조).
```env
# Example .env
# PROJECT_ROOT=... (Optional)
```

---

## 🚀 Execution Guide

프로젝트는 다음 순서로 실행하는 것을 권장합니다:

1. **Data Preprocessing**: `notebooks/data.ipynb` 및 `data_for_seoul/mapo.ipynb`를 실행하여 원천 데이터를 정제하고 GeoDataFrame으로 변환합니다.
2. **Model Training**: `notebooks/train.ipynb`를 실행하여 고위험군 예측 모델을 학습합니다.
3. **Visualization**: `notebooks/result_visualization.ipynb`를 실행하여 예측 결과와 쓰레기통 위치 데이터를 시각화합니다.

---