# 우리 지역 체크인 📍

이름·지역·만족도·메모를 입력해 방문 기록을 남기는 위치 기반 체크인 서비스입니다.
기록은 서버 파일에 저장되어 새로고침해도 사라지지 않고, 통계·검색·CSV 내보내기까지 지원합니다.
FastAPI 백엔드와 Streamlit 프런트엔드로 구성된 실습용 프로젝트입니다.

## 주요 기능

- **방문 기록 입력**: 이름 / 지역 / 만족도(1~5) / 한 줄 메모를 폼으로 입력하고 저장
- **기록 저장(JSONL)**: 저장된 기록은 `backend/data/records.jsonl` 파일에 영구 저장
- **전체 기록 조회**: 저장된 모든 기록을 표로 확인
- **사용자별 조회**: 이름으로 내가 남긴 기록만 조회, 기록 수·평균 만족도 확인
- **기록 삭제**: 잘못 남긴 기록을 id로 삭제
- **지역별 통계 대시보드**: 총 기록 수, 참여자 수, 전체 평균 만족도, 지역별 평균 만족도 그래프
- **검색·필터**: 지역 / 최소 만족도 / 메모 키워드로 기록 필터링 (사이드바)
- **CSV 내보내기**: 필터가 적용된 기록을 한글이 깨지지 않는 CSV로 다운로드
- **탭 기반 화면 구성**: "기록 남기기" / "내 기록" / "전체 현황" 3개 탭으로 화면 정리
- (데모) 지역 선택 시 랜덤 좌표를 지도와 그래프에 표시하는 실습 시작 코드 기능

## 프로젝트 구조

```
backend/    FastAPI 백엔드 (main.py, requirements.txt)
frontend/   Streamlit 프런트엔드 (app.py, requirements.txt)
```

## 로컬에서 실행하는 방법

### 1. conda 환경 만들기

```bash
conda create -n checkin python=3.11 -y
conda activate checkin
```

### 2. 의존성 설치

```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 3. 백엔드 실행 (터미널 1)

```bash
cd backend
uvicorn main:app --reload --port 8000
```

- API 문서: http://localhost:8000/docs

### 4. 프런트엔드 실행 (터미널 2)

```bash
cd frontend
streamlit run app.py
```

- 화면 접속: http://localhost:8501

> 프런트는 기본적으로 `http://localhost:8000` 백엔드를 바라봅니다. 주소를 바꾸려면 `BACKEND_URL` 환경변수를 설정하세요.
