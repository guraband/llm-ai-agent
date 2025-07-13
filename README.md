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
python -m venv .venv

# (macOS/Linux)
source .venv/bin/activate

# (Windows)
.venv\Scripts\activate
```

가상환경이 활성화된 상태에서 위의 uv 명령어를 실행하세요.
