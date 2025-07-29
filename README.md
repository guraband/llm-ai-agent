### _'Do it! LLM을 활용한 AI 에이전트 개발 입문'_ 실습 프로젝트

---

## 설치 및 실행 안내

### 1. uv를 사용한 패키지 설치
이 프로젝트는 [uv](https://github.com/astral-sh/uv)를 사용하여 패키지를 설치합니다. uv는 빠르고 효율적인 Python 패키지 매니저입니다.

```bash
# uv 설치 (최초 1회)
pip install uv

# 의존성 설치
uv pip install -r requirements.txt
```

### 2. 가상환경 생성 및 활성화
권장: Python 가상환경(venv) 사용

```bash
# 가상환경 생성 (예시: .venv 폴더에 생성)
source .venv/bin/activate
```

가상환경이 활성화된 상태에서 위의 uv 명령어를 실행하세요.

### 3. Streamlit 웹 앱 실행

#### 3.1 Streamlit 설치
```bash
# Streamlit 추가 설치
uv add streamlit
```

#### 3.2 웹 앱 실행
```bash
# Chapter 07 - AI 에이전트 채팅 앱 실행
uv run streamlit run chapter07/now.py
```

#### 3.3 웹 브라우저 접속
- 실행 후 브라우저에서 `http://localhost:8501` 접속
- 💬 Chatbot 인터페이스를 통해 AI와 대화 가능
- "서울은 몇시야?" 같은 시간 관련 질문 테스트 가능

#### 3.4 앱 종료
- 터미널에서 `Ctrl + C`로 앱 종료

### 4. 예제 소스
- [github](https://github.com/saintdragon2/gpt_agent_2025_easyspub)